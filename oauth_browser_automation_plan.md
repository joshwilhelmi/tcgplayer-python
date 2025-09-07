# TCGplayer Store OAuth Browser Automation Plan

## Overview

This document outlines the implementation plan for TCGplayer Store Authorization using browser automation in the future MCP server integration. The current TCGplayer Client library provides all necessary endpoints, but the OAuth flow requires browser interaction that is impractical for testing.

## Current Limitation

The TCGplayer Store Authorization workflow requires:

1. **Manual Browser Interaction**: Store owner must log into TCGplayer store admin
2. **6-Digit Authorization Code**: Short-lived (1 hour) code generated after manual approval
3. **Complex Token Exchange**: Multiple API calls to convert codes to bearer tokens
4. **Store Credentials**: Requires actual store owner login credentials

## OAuth Workflow Steps

### Phase 1: Authorization Request
```
1. Present "Connect to TCGplayer" button to store owner
2. Redirect to: https://store.tcgplayer.com/admin/Apps/{PublicKey}
3. Store owner logs in with credentials
4. Store owner reviews application permissions
5. Store owner approves/denies application access
```

### Phase 2: Code Exchange
```
6. TCGplayer generates 6-digit Authorization Code (1-hour validity)
7. Application captures authorization code automatically
8. POST to: https://api.tcgplayer.com/app/authorize/{code}
9. Receive ACCESS_TOKEN response
```

### Phase 3: Bearer Token Generation  
```
10. POST to: https://api.tcgplayer.com/token/access
11. Headers: X-Tcg-Access-Token: {ACCESS_TOKEN}
12. Receive Bearer Token for API requests
13. Verify store identity: GET https://api.tcgplayer.com/stores/self
```

## MCP Server Implementation Plan

### Technology Stack
- **Browser Automation**: Playwright or Selenium WebDriver
- **MCP Framework**: Model Context Protocol server implementation
- **Security**: Secure token storage and rotation
- **Error Handling**: Robust retry logic and fallback mechanisms

### Implementation Architecture

```python
class TCGplayerMCPServer:
    """MCP Server with TCGplayer Store OAuth automation."""
    
    async def authenticate_store(self, store_credentials: Dict[str, str]) -> str:
        """
        Automate the complete store authorization workflow.
        
        Args:
            store_credentials: {"username": "...", "password": "..."}
            
        Returns:
            bearer_token: Valid bearer token for store operations
        """
        
    async def _browser_oauth_flow(self, credentials: Dict) -> str:
        """Handle browser automation for OAuth flow."""
        
    async def _exchange_authorization_code(self, code: str) -> str:
        """Exchange 6-digit code for ACCESS_TOKEN."""
        
    async def _generate_bearer_token(self, access_token: str) -> str:
        """Generate bearer token from ACCESS_TOKEN."""
```

### Security Considerations

1. **Credential Protection**
   - Store credentials encrypted at rest
   - Use secure key derivation (PBKDF2/Argon2)
   - Never log credentials in plain text
   - Implement credential rotation

2. **Token Management**
   - Secure bearer token storage
   - Automatic token refresh before expiry
   - Token revocation on security events
   - Audit logging for all token operations

3. **Browser Automation Security**
   - Headless browser execution
   - Network isolation and VPN support
   - Screenshot capture for debugging (sanitized)
   - Automatic cleanup of browser sessions

### Error Handling Strategy

```python
class OAuthFlowHandler:
    """Robust error handling for OAuth flow."""
    
    async def handle_expired_code(self) -> bool:
        """Handle 1-hour code expiry - restart flow."""
        
    async def handle_login_failure(self) -> bool:
        """Handle store login failures - retry with backoff."""
        
    async def handle_network_errors(self) -> bool:
        """Handle network timeouts - retry with circuit breaker."""
        
    async def handle_captcha_challenges(self) -> bool:
        """Handle potential CAPTCHA challenges - manual intervention."""
```

### Integration Points

#### Current TCGplayer Client Integration
```python
# The existing client library is ready for bearer tokens
config = ClientConfig(
    client_id=client_id,
    client_secret=client_secret,
    bearer_token=bearer_token  # From MCP OAuth flow
)

async with TCGplayerClient(config=config) as client:
    # All store operations now available
    inventory = await client.endpoints.inventory.get_productlist_by_id(123)
    orders = await client.endpoints.stores.get_store_orders(store_key)
```

#### MCP Server Tool Integration
```python
@mcp_tool("tcgplayer_get_store_inventory")
async def get_store_inventory(store_key: str) -> Dict:
    """Get store inventory via authenticated API."""
    bearer_token = await oauth_handler.get_valid_bearer_token()
    async with TCGplayerClient(bearer_token=bearer_token) as client:
        return await client.endpoints.inventory.get_productlist_by_id(store_key)
```

### Testing Strategy

1. **Staging Environment Testing**
   - Use TCGplayer sandbox/staging environment if available
   - Create test store accounts for automation testing
   - Implement comprehensive integration tests

2. **Production Validation**
   - Gradual rollout with monitoring
   - Comprehensive logging and alerting
   - Fallback to manual OAuth for critical failures

3. **Continuous Monitoring**
   - Token validity monitoring
   - OAuth flow success rates
   - Performance metrics and latency tracking

## Implementation Timeline

### Phase 1: MCP Server Foundation (Week 1-2)
- Set up MCP server framework
- Implement basic TCGplayer client integration
- Create secure configuration management

### Phase 2: Browser Automation (Week 3-4)  
- Implement Playwright/Selenium integration
- Create OAuth flow automation
- Add comprehensive error handling

### Phase 3: Security & Testing (Week 5-6)
- Implement token security measures
- Create comprehensive test suite  
- Add monitoring and alerting

### Phase 4: Production Integration (Week 7-8)
- Deploy to staging environment
- Conduct load testing and security review
- Production deployment with monitoring

## Benefits of This Approach

1. **Complete API Coverage**: Access to all 80 TCGplayer endpoints
2. **Automated Workflows**: No manual intervention for routine operations  
3. **Security Best Practices**: Enterprise-grade security and token management
4. **Scalability**: Support multiple stores and concurrent operations
5. **Monitoring**: Comprehensive logging and error tracking
6. **Future-Proof**: Easy to extend for additional TCGplayer features

## Current Status

- **TCGplayer Client**: ✅ Complete (all 80 endpoints implemented)
- **Public API Testing**: ✅ Complete (43 endpoints fully tested)
- **OAuth Documentation**: ✅ Complete (workflow documented)
- **MCP Server**: ⏳ Planned (browser automation implementation)
- **Production Deployment**: ⏳ Future (after MCP server completion)

## Next Steps

1. Complete current TCGplayer Client library testing and documentation
2. Begin MCP server framework development
3. Implement browser automation for OAuth workflow
4. Create comprehensive test suite for store operations
5. Deploy and monitor production integration

---

*This plan provides a clear roadmap for implementing TCGplayer Store OAuth automation while maintaining security, reliability, and scalability.*