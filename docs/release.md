## Release 0.3.0 — Openapi® Python SDK Evolves

The **0.3.0** release of the Openapi® Python SDK introduces powerful new features, critical bug fixes, and significant stability improvements that make it even easier to build robust and reliable API clients.

### 🚀 New Features

* **Async Support & Context Managers**: Full `httpx`-based async client support with context manager support for all clients, enabling modern asynchronous Python workflows.
* **Configurable Timeouts**: Added configurable 30-second default timeouts for both sync and async clients, with the ability to customize timeout values during OAuth client initialization.
* **Thread-Safe OAuth Client**: `OauthClient` is now thread-safe using `threading.local`, allowing shared instances across multiple threads without conflicts.
* **Custom HTTP Client Injection**: Advanced users can now inject custom HTTP clients for tailored transport layers and retry configurations.
* **Refactored Architecture**: Client classes have been extracted into separate module files without breaking the existing API, improving maintainability and clarity.

### 🔧 Bug Fixes

* **Query Parameter Encoding**: Fixed an issue where special characters in query parameters caused `400 Bad Request` errors by properly encoding them with `urllib`.
* **Linting & Tests**: Resolved ruff formatting issues and cleaned up unused variables in test suites.

### 🧪 Quality & Testing

* Added a comprehensive thread-safety verification suite for synchronous clients.
* Updated documentation with examples for configuring network timeouts and customizing transport layers.

### 🎯 Why This Matters

* Safer concurrent usage with thread-safe OAuth handling.
* Greater control over network behavior with configurable timeouts and custom HTTP clients.
* More predictable request handling with properly encoded query parameters.
* Cleaner codebase architecture for easier future contributions.

### 🙏 Special Thanks

A huge thank you to **[@Deadpool2000](https://github.com/Deadpool2000)** for their outstanding contributions to this release. Their work on thread-safety, configurable timeouts, custom HTTP client support, query parameter encoding fixes, and overall code quality has been invaluable. This release would not have been possible without their dedication and effort.

### 🚀 Looking Ahead

Version **0.3.0** marks another major step toward a more mature and developer-friendly Python SDK. Future releases will continue to focus on performance enhancements, broader interoperability, and even more seamless developer experiences.
