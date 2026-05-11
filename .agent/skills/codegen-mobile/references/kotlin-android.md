# Kotlin / Android (Jetpack Compose) Reference

## Project structure

```
app/src/main/
  kotlin/com/example/app/
    ui/
      screens/        # Composable screen functions
      components/     # Reusable composables
      theme/          # Material3 theme
    viewmodel/        # @HiltViewModel classes
    data/
      repository/     # Repository pattern
      remote/         # Retrofit API services
      local/          # Room DAOs
    di/               # Hilt modules
  res/
    values/           # strings.xml, colors.xml
```

## State management (ViewModel + StateFlow)

```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UserUiState>(UserUiState.Loading)
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    fun loadUser(id: String) {
        viewModelScope.launch {
            _uiState.value = UserUiState.Loading
            userRepository.getUser(id)
                .onSuccess { user -> _uiState.value = UserUiState.Success(user) }
                .onFailure { error -> _uiState.value = UserUiState.Error(error.message ?: "Unknown error") }
        }
    }
}

sealed class UserUiState {
    data object Loading : UserUiState()
    data class Success(val user: User) : UserUiState()
    data class Error(val message: String) : UserUiState()
}
```

## Screen composable

```kotlin
@Composable
fun UserScreen(
    viewModel: UserViewModel = hiltViewModel(),
    onNavigateBack: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("User Profile") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues)) {
            when (val state = uiState) {
                is UserUiState.Loading -> CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                is UserUiState.Error -> ErrorMessage(message = state.message, onRetry = { viewModel.loadUser(userId) })
                is UserUiState.Success -> UserContent(user = state.user)
            }
        }
    }
}
```

## Navigation (Compose Navigation)

```kotlin
@Composable
fun AppNavGraph(navController: NavHostController) {
    NavHost(navController, startDestination = "home") {
        composable("home") {
            HomeScreen(onNavigateToUser = { id -> navController.navigate("user/$id") })
        }
        composable("user/{userId}", arguments = listOf(navArgument("userId") { type = NavType.StringType })) { backStack ->
            val userId = backStack.arguments?.getString("userId")!!
            UserScreen(userId = userId, onNavigateBack = { navController.popBackStack() })
        }
    }
}
```

## Hilt dependency injection

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides @Singleton
    fun provideRetrofit(): Retrofit = Retrofit.Builder()
        .baseUrl(BuildConfig.API_BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    @Provides @Singleton
    fun provideUserApi(retrofit: Retrofit): UserApi = retrofit.create(UserApi::class.java)
}
```
