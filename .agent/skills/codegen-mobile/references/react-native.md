# React Native Reference

## Project setup (Expo recommended)

```bash
npx create-expo-app MyApp --template blank-typescript
```

```
src/
  screens/          # Screen components
  components/       # Reusable UI components
  navigation/       # React Navigation config
  hooks/            # Custom hooks (useAuth, useApi)
  services/         # API client, storage
  stores/           # Zustand or Redux state
  types/            # TypeScript types
```

## Navigation (React Navigation v7)

```typescript
// navigation/types.ts
export type RootStackParamList = {
  Home: undefined;
  UserDetail: { userId: string };
  Settings: undefined;
};

// navigation/AppNavigator.tsx
import { createNativeStackNavigator } from '@react-navigation/native-stack';
const Stack = createNativeStackNavigator<RootStackParamList>();

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="UserDetail" component={UserDetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## State management (Zustand)

```typescript
import { create } from 'zustand';

interface UserStore {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  loadUser: (id: string) => Promise<void>;
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  isLoading: false,
  error: null,
  loadUser: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const user = await userApi.getUser(id);
      set({ user, isLoading: false });
    } catch (err) {
      set({ error: 'Failed to load user', isLoading: false });
    }
  },
}));
```

## Screen structure with loading/error states

```typescript
import { useEffect } from 'react';
import { View, Text, ActivityIndicator, Pressable } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';

type Props = NativeStackScreenProps<RootStackParamList, 'UserDetail'>;

export function UserDetailScreen({ route }: Props) {
  const { userId } = route.params;
  const { user, isLoading, error, loadUser } = useUserStore();

  useEffect(() => { loadUser(userId); }, [userId]);

  if (isLoading) return <ActivityIndicator style={styles.center} />;
  if (error) return (
    <View style={styles.center}>
      <Text>{error}</Text>
      <Pressable onPress={() => loadUser(userId)}><Text>Retry</Text></Pressable>
    </View>
  );
  if (!user) return null;

  return (
    <View style={styles.container}>
      <Text style={styles.name}>{user.name}</Text>
      <Text>{user.email}</Text>
    </View>
  );
}
```

## Persistent storage (MMKV)

```typescript
import { MMKV } from 'react-native-mmkv';
export const storage = new MMKV();

// Use
storage.set('auth_token', token);
const token = storage.getString('auth_token');
```

## Accessibility

```typescript
<Pressable
  accessible
  accessibilityLabel="Submit form"
  accessibilityRole="button"
  accessibilityState={{ disabled: isLoading }}
  onPress={handleSubmit}
>
  <Text>Submit</Text>
</Pressable>
```
