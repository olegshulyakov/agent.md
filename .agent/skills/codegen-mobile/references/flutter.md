# Flutter Reference

## Project structure

```
lib/
  main.dart
  app/
    router.dart           # go_router config
    theme.dart            # Material theme
  features/
    user/
      data/
        user_repository.dart
        user_api.dart
      domain/
        user.dart          # Freezed model
      presentation/
        user_screen.dart
        user_notifier.dart # Riverpod StateNotifier
  core/
    widgets/              # Shared widgets
    services/             # DI, storage, http
```

## State management (Riverpod)

```dart
// user_notifier.dart
@riverpod
class UserNotifier extends _$UserNotifier {
  @override
  FutureOr<User> build(String userId) async {
    return ref.watch(userRepositoryProvider).getUser(userId);
  }
}

// Usage in widget:
class UserScreen extends ConsumerWidget {
  const UserScreen({required this.userId, super.key});
  final String userId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userNotifierProvider(userId));
    return Scaffold(
      appBar: AppBar(title: const Text('User Profile')),
      body: userAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, _) => Center(
          child: Column(children: [
            Text('Error: $err'),
            ElevatedButton(
              onPressed: () => ref.invalidate(userNotifierProvider(userId)),
              child: const Text('Retry'),
            ),
          ]),
        ),
        data: (user) => UserContent(user: user),
      ),
    );
  }
}
```

## Navigation (go_router)

```dart
// router.dart
final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(path: '/', builder: (ctx, state) => const HomeScreen()),
      GoRoute(
        path: '/users/:id',
        builder: (ctx, state) => UserScreen(userId: state.pathParameters['id']!),
      ),
    ],
  );
});

// Navigate
context.push('/users/$userId');
context.go('/home');
```

## Freezed models

```dart
// user.dart
import 'package:freezed_annotation/freezed_annotation.dart';
part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String email,
    required String name,
    @Default('viewer') String role,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

## HTTP client (Dio)

```dart
@riverpod
Dio dio(DioRef ref) {
  final dio = Dio(BaseOptions(baseUrl: 'https://api.example.com'));
  dio.interceptors.add(
    InterceptorsWrapper(
      onRequest: (options, handler) {
        final token = ref.read(authTokenProvider);
        if (token != null) options.headers['Authorization'] = 'Bearer $token';
        handler.next(options);
      },
    ),
  );
  return dio;
}
```

## Accessibility

```dart
Semantics(
  label: 'Submit registration form',
  button: true,
  enabled: !isLoading,
  child: ElevatedButton(onPressed: isLoading ? null : handleSubmit, child: const Text('Submit')),
)
```
