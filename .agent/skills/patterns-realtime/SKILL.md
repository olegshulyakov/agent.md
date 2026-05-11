---
name: patterns-realtime
description: >
  Produces real-time communication pattern guides with WebSocket, Server-Sent Events (SSE), and polling
  strategy selection, including implementation examples and trade-off analysis. Use this skill whenever
  the user wants to add real-time features, implement live updates, choose between WebSocket and SSE,
  build a chat system, add live notifications, implement collaborative features, or asks "should I use
  WebSocket or SSE", "how do I implement real-time updates", "add live data to my app", "implement
  WebSocket in Node.js", "how does SSE work", "build a live feed", or "add push notifications to my API".
  Also trigger for "long polling vs WebSocket", "Socket.io setup", "real-time collaboration", and
  "server push". Distinct from patterns-graphql (GraphQL subscriptions specifically) and codegen-backend
  (general backend code generation).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# patterns-realtime

Produce **real-time communication patterns** with trade-off analysis and implementation examples for WebSocket, SSE, and polling.

## Strategy Selection

Choose based on the use case:

| Criteria | WebSocket | SSE | Long Polling | Short Polling |
|----------|-----------|-----|-------------|--------------|
| **Direction** | Bidirectional | Server → Client | Server → Client | Server → Client |
| **Latency** | Very low | Low | Medium | High |
| **Server load** | High (persistent conn) | Medium (persistent) | Medium | Low per request |
| **Complexity** | High | Low | Medium | Lowest |
| **Browser support** | Universal | Universal (no IE) | Universal | Universal |
| **Firewall friendly** | Sometimes not | Yes (HTTP) | Yes | Yes |
| **Auto-reconnect** | Manual | Built-in | Manual | Implicit |
| **Use when** | Chat, collab, gaming | Live feeds, notifications | Simple push needs | Polling acceptable |

**Decision guide:**
- **Need bidirectional communication?** → WebSocket
- **Server-to-client only, want simplicity?** → SSE
- **Can't use WebSocket, need fallback?** → SSE or Long Polling
- **Real-time is nice-to-have, data changes rarely?** → Short Polling

## WebSocket Implementation

### Server (Node.js / ws library)

```typescript
import { WebSocketServer, WebSocket } from 'ws';
import { IncomingMessage } from 'http';
import { parse } from 'url';

// Connection registry
const rooms = new Map<string, Set<WebSocket>>();
const clientMeta = new Map<WebSocket, { userId: string; roomId: string }>();

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws: WebSocket, req: IncomingMessage) => {
  // Authentication
  const { query } = parse(req.url!, true);
  const userId = authenticate(query.token as string);
  if (!userId) { ws.close(4001, 'Unauthorized'); return; }

  const roomId = query.room as string || 'default';
  
  // Join room
  if (!rooms.has(roomId)) rooms.set(roomId, new Set());
  rooms.get(roomId)!.add(ws);
  clientMeta.set(ws, { userId, roomId });

  // Heartbeat to detect dead connections
  (ws as any).isAlive = true;
  ws.on('pong', () => { (ws as any).isAlive = true; });

  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data.toString());
      handleMessage(ws, message, userId, roomId);
    } catch {
      ws.send(JSON.stringify({ type: 'error', message: 'Invalid JSON' }));
    }
  });

  ws.on('close', () => {
    rooms.get(roomId)?.delete(ws);
    clientMeta.delete(ws);
  });

  ws.send(JSON.stringify({ type: 'connected', userId, roomId }));
});

// Heartbeat interval — remove dead connections
const heartbeat = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!(ws as any).isAlive) { ws.terminate(); return; }
    (ws as any).isAlive = false;
    ws.ping();
  });
}, 30_000);

wss.on('close', () => clearInterval(heartbeat));

function broadcast(roomId: string, message: object, exclude?: WebSocket) {
  const clients = rooms.get(roomId) ?? new Set();
  const payload = JSON.stringify(message);
  for (const client of clients) {
    if (client !== exclude && client.readyState === WebSocket.OPEN) {
      client.send(payload);
    }
  }
}

function handleMessage(ws: WebSocket, msg: any, userId: string, roomId: string) {
  switch (msg.type) {
    case 'chat:message':
      broadcast(roomId, { type: 'chat:message', userId, text: msg.text, ts: Date.now() }, ws);
      break;
    case 'typing:start':
      broadcast(roomId, { type: 'typing:start', userId }, ws);
      break;
    // Add more message types as needed
  }
}
```

### Client (Browser)

```typescript
class RealtimeClient {
  private ws: WebSocket | null = null;
  private reconnectDelay = 1000;
  private maxReconnectDelay = 30_000;
  private listeners = new Map<string, Set<Function>>();

  connect(url: string) {
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      this.reconnectDelay = 1000; // Reset on success
      this.emit('connected');
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.emit(message.type, message);
    };

    this.ws.onclose = (event) => {
      if (event.code !== 1000) {
        setTimeout(() => {
          this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);
          this.connect(url); // Exponential backoff reconnect
        }, this.reconnectDelay);
      }
    };
  }

  send(type: string, payload: object) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, ...payload }));
    }
  }

  on(event: string, handler: Function) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event)!.add(handler);
  }

  private emit(event: string, data?: any) {
    this.listeners.get(event)?.forEach(fn => fn(data));
  }

  disconnect() { this.ws?.close(1000); }
}
```

## SSE Implementation

### Server (Express)

```typescript
import express from 'express';

const app = express();
const clients = new Map<string, express.Response>(); // userId → response

app.get('/events', (req, res) => {
  const userId = authenticate(req.headers.authorization);
  if (!userId) { res.sendStatus(401); return; }

  // SSE headers
  res.set({
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no', // Disable Nginx buffering
  });
  res.flushHeaders();

  clients.set(userId, res);

  // Send initial connection event
  sendEvent(res, 'connected', { userId });

  // Heartbeat to keep connection alive through proxies
  const heartbeat = setInterval(() => {
    res.write(':heartbeat\n\n');
  }, 15_000);

  req.on('close', () => {
    clearInterval(heartbeat);
    clients.delete(userId);
  });
});

function sendEvent(res: express.Response, event: string, data: object) {
  res.write(`event: ${event}\n`);
  res.write(`data: ${JSON.stringify(data)}\n\n`);
}

function pushToUser(userId: string, event: string, data: object) {
  const client = clients.get(userId);
  if (client) sendEvent(client, event, data);
}

// Usage: push notification when something happens
async function onOrderShipped(orderId: string, userId: string) {
  pushToUser(userId, 'order:shipped', { orderId, timestamp: Date.now() });
}
```

### Client (Browser)

```typescript
class SSEClient {
  private eventSource: EventSource | null = null;

  connect(url: string) {
    this.eventSource = new EventSource(url, { withCredentials: true });

    // Listen for specific named events
    this.eventSource.addEventListener('order:shipped', (e) => {
      const data = JSON.parse(e.data);
      console.log('Order shipped:', data);
    });

    this.eventSource.addEventListener('notification', (e) => {
      showNotification(JSON.parse(e.data));
    });

    this.eventSource.onerror = (err) => {
      // EventSource auto-reconnects — handle state if needed
      console.warn('SSE error, will reconnect:', err);
    };
  }

  disconnect() {
    this.eventSource?.close();
  }
}
```

## Polling Patterns

```typescript
// Short polling — simple, works everywhere
function startPolling(url: string, interval = 5000) {
  let timeoutId: number;

  async function poll() {
    try {
      const res = await fetch(url);
      const data = await res.json();
      handleUpdate(data);
    } finally {
      timeoutId = setTimeout(poll, interval);
    }
  }

  poll();
  return () => clearTimeout(timeoutId);
}

// Long polling — server holds request until data available
async function longPoll(url: string, lastEventId: string) {
  while (true) {
    try {
      const res = await fetch(`${url}?after=${lastEventId}`, {
        signal: AbortSignal.timeout(30_000)
      });
      const { events, lastId } = await res.json();
      if (events.length) {
        handleEvents(events);
        lastEventId = lastId;
      }
    } catch (err) {
      if (err.name !== 'TimeoutError') {
        await sleep(2000); // Back off on actual errors
      }
      // Timeout = no new events, loop again immediately
    }
  }
}
```

## Scaling Considerations

For multi-server deployments, you need a pub/sub layer:

```typescript
// Redis pub/sub for horizontal scaling
import { createClient } from 'redis';

const pub = createClient({ url: process.env.REDIS_URL });
const sub = pub.duplicate();

await Promise.all([pub.connect(), sub.connect()]);

// Subscribe to user-specific channels
await sub.subscribe(`user:${userId}:events`, (message) => {
  const event = JSON.parse(message);
  pushToUser(userId, event.type, event.data);
});

// Publish from any server instance
async function broadcastToUser(userId: string, type: string, data: object) {
  await pub.publish(`user:${userId}:events`, JSON.stringify({ type, data }));
}
```

## Calibration

- **Use case is notifications**: SSE is usually simpler and sufficient
- **Use case is chat/collab**: WebSocket; show bidirectional message handling
- **Need to pick a pattern**: Show the decision table and ask one clarifying question (direction of data flow)
- **Existing code, add real-time**: Retrofit SSE onto existing REST endpoint; minimal changes
- **Scaling question**: Show Redis pub/sub pattern
