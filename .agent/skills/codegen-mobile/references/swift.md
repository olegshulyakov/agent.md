# Swift / SwiftUI Reference

## Project setup

```
Package.swift — Swift Package Manager
Sources/
  AppName/
    App.swift               # @main entry point
    Views/                  # SwiftUI views
    ViewModels/             # @Observable or ObservableObject classes
    Models/                 # Data models
    Services/               # Network, persistence
    Extensions/             # Swift extensions
```

## State management

```swift
// Modern: @Observable (Swift 5.9+, iOS 17+)
@Observable class UserViewModel {
    var user: User?
    var isLoading = false
    var error: Error?
    
    func loadUser(id: String) async {
        isLoading = true
        defer { isLoading = false }
        do {
            user = try await userService.fetchUser(id: id)
        } catch {
            self.error = error
        }
    }
}

// Usage in view:
struct UserView: View {
    @State private var viewModel = UserViewModel()
    
    var body: some View {
        Group {
            if viewModel.isLoading { ProgressView() }
            else if let error = viewModel.error { ErrorView(error: error) }
            else if let user = viewModel.user { UserContentView(user: user) }
        }
        .task { await viewModel.loadUser(id: "123") }
    }
}
```

## Navigation (NavigationStack)

```swift
// App entry
NavigationStack(path: $router.path) {
    HomeView()
        .navigationDestination(for: Route.self) { route in
            switch route {
            case .userDetail(let id): UserDetailView(userId: id)
            case .settings: SettingsView()
            }
        }
}

enum Route: Hashable {
    case userDetail(id: String)
    case settings
}
```

## Networking (async/await)

```swift
struct APIClient {
    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let (data, response) = try await URLSession.shared.data(for: endpoint.request)
        guard let http = response as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            throw APIError.badResponse
        }
        return try JSONDecoder().decode(T.self, from: data)
    }
}
```

## Dependency injection (via environment)

```swift
// Define
struct APIClientKey: EnvironmentKey {
    static let defaultValue = APIClient()
}

extension EnvironmentValues {
    var apiClient: APIClient {
        get { self[APIClientKey.self] }
        set { self[APIClientKey.self] = newValue }
    }
}

// Inject at root
ContentView().environment(\.apiClient, APIClient(baseURL: URL(string: "https://api.example.com")!))

// Use in view
@Environment(\.apiClient) private var apiClient
```

## Accessibility

```swift
Image(systemName: "star.fill")
    .accessibilityLabel("Favorite")
    .accessibilityHint("Double tap to remove from favorites")

Button("Submit") { ... }
    .accessibilityAddTraits(.isButton)
    .accessibilityIdentifier("submitButton") // for UI testing
```
