#!/usr/bin/env python3
"""
TPS_1773321224_26359 MCP Server - FastMCP with D402 Transport Wrapper

Uses FastMCP from official MCP SDK with D402MCPTransport wrapper for HTTP 402.

Architecture:
- FastMCP for tool decorators and Context objects
- D402MCPTransport wraps the /mcp route for HTTP 402 interception
- Proper HTTP 402 status codes (not JSON-RPC wrapped)

Generated from OpenAPI: None

Environment Variables:
- SERVER_ADDRESS: Payment address (IATP wallet contract)
- MCP_OPERATOR_PRIVATE_KEY: Operator signing key
- D402_TESTING_MODE: Skip facilitator (default: true)
"""

import os
import logging
import sys
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, Union
from datetime import datetime

import requests
from retry import retry
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('tps-1773321224-26359_mcp')

# FastMCP from official SDK
from mcp.server.fastmcp import FastMCP, Context
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

# D402 payment protocol - using Starlette middleware
from traia_iatp.d402.starlette_middleware import D402PaymentMiddleware
from traia_iatp.d402.mcp_middleware import require_payment_for_tool, get_active_api_key
from traia_iatp.d402.payment_introspection import extract_payment_configs_from_mcp
from traia_iatp.d402.types import TokenAmount, TokenAsset, EIP712Domain

# Configuration
STAGE = os.getenv("STAGE", "MAINNET").upper()
PORT = int(os.getenv("PORT", "8000"))
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
if not SERVER_ADDRESS:
    raise ValueError("SERVER_ADDRESS required for payment protocol")

API_KEY = None

logger.info("="*80)
logger.info(f"TPS_1773321224_26359 MCP Server (FastMCP + D402 Wrapper)")
logger.info(f"API: https://petstore3.swagger.io/api/v3")
logger.info(f"Payment: {SERVER_ADDRESS}")
logger.info("="*80)

# Create FastMCP server
mcp = FastMCP("TPS_1773321224_26359 MCP Server", host="0.0.0.0")

logger.info(f"✅ FastMCP server created")

# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================
# Tool implementations will be added here by endpoint_implementer_crew
# Each tool will use the @mcp.tool() and @require_payment_for_tool() decorators


# D402 Payment Middleware
# The HTTP 402 payment protocol middleware is already configured in the server initialization.
# It's imported from traia_iatp.d402.mcp_middleware and auto-detects configuration from:
# - PAYMENT_ADDRESS or EVM_ADDRESS: Where to receive payments
# - EVM_NETWORK: Blockchain network (default: base-sepolia)
# - DEFAULT_PRICE_USD: Price per request (default: $0.001)
# - TPS_1773321224_26359_API_KEY: Server's internal API key for payment mode
#
# All payment verification logic is handled by the traia_iatp.d402 module.
# No custom implementation needed!


# API Endpoint Tool Implementations

@mcp.tool()
@require_payment_for_tool(
    price=TokenAmount(
        amount="10000",  # 0.01 tokens
        asset=TokenAsset(
            address="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
            decimals=6,
            network="sepolia",
            eip712=EIP712Domain(
                name="IATPWallet",
                version="1"
            )
        )
    ),
    description="Multiple status values can be provided with comma "

)
async def finds_pets_by_status(
    context: Context,
    status: str = "available"
) -> Any:
    """
    Multiple status values can be provided with comma separated strings.

    Generated from OpenAPI endpoint: GET /pet/findByStatus

    Args:
        context: MCP context (auto-injected by framework, not user-provided)
        status: Status values that need to be considered for filter (optional, default: "available")

    Returns:
        API response (dict, list, or other JSON type)

    Example Usage:
        await finds_pets_by_status(status="available")

        Note: 'context' parameter is auto-injected by MCP framework
    """
    # Payment already verified by @require_payment_for_tool decorator
    # No authentication required for this API - api_key not needed

    try:
        url = f"https://petstore3.swagger.io/api/v3/pet/findByStatus"
        params = {
            "status": status
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {}
        # No auth required for this API

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        logger.error(f"Error in finds_pets_by_status: {e}")
        return {"error": str(e), "endpoint": "/pet/findByStatus"}


@mcp.tool()
@require_payment_for_tool(
    price=TokenAmount(
        amount="10000",  # 0.01 tokens
        asset=TokenAsset(
            address="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
            decimals=6,
            network="sepolia",
            eip712=EIP712Domain(
                name="IATPWallet",
                version="1"
            )
        )
    ),
    description="For valid response try integer IDs with value <= 5"

)
async def find_purchase_order_by_id(
    context: Context,
    orderId: int
) -> Any:
    """
    For valid response try integer IDs with value <= 5 or > 10. Other values will generate exceptions.

    Generated from OpenAPI endpoint: GET /store/order/{orderId}

    Args:
        context: MCP context (auto-injected by framework, not user-provided)
        orderId: ID of order that needs to be fetched (optional)

    Returns:
        API response (dict, list, or other JSON type)

    Example Usage:
        await find_purchase_order_by_id(orderId=1)

        Note: 'context' parameter is auto-injected by MCP framework
    """
    # Payment already verified by @require_payment_for_tool decorator
    # No authentication required for this API - api_key not needed

    try:
        url = f"https://petstore3.swagger.io/api/v3/store/order/{orderId}"
        params = {}
        headers = {}
        # No auth required for this API

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        logger.error(f"Error in find_purchase_order_by_id: {e}")
        return {"error": str(e), "endpoint": "/store/order/{orderId}"}


@mcp.tool()
@require_payment_for_tool(
    price=TokenAmount(
        amount="10000",  # 0.01 tokens
        asset=TokenAsset(
            address="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
            decimals=6,
            network="sepolia",
            eip712=EIP712Domain(
                name="IATPWallet",
                version="1"
            )
        )
    ),
    description="For valid response try integer IDs with value < 10"

)
async def delete_purchase_order_by_identifier(
    context: Context,
    orderId: int
) -> Any:
    """
    For valid response try integer IDs with value < 1000. Anything above 1000 or non-integers will generate API errors.

    Generated from OpenAPI endpoint: DELETE /store/order/{orderId}

    Args:
        context: MCP context (auto-injected by framework, not user-provided)
        orderId: ID of the order that needs to be deleted (optional)

    Returns:
        API response (dict, list, or other JSON type)

    Example Usage:
        await delete_purchase_order_by_identifier(orderId=1)

        Note: 'context' parameter is auto-injected by MCP framework
    """
    # Payment already verified by @require_payment_for_tool decorator
    # No authentication required for this API - api_key not needed

    try:
        url = f"https://petstore3.swagger.io/api/v3/store/order/{orderId}"
        params = {}
        headers = {}
        # No auth required for this API

        response = requests.delete(
            url,
            params=params,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        logger.error(f"Error in delete_purchase_order_by_identifier: {e}")
        return {"error": str(e), "endpoint": "/store/order/{orderId}"}


@mcp.tool()
@require_payment_for_tool(
    price=TokenAmount(
        amount="10000",  # 0.01 tokens
        asset=TokenAsset(
            address="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
            decimals=6,
            network="sepolia",
            eip712=EIP712Domain(
                name="IATPWallet",
                version="1"
            )
        )
    ),
    description="Log into the system."

)
async def logs_user_into_the_system(
    context: Context,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Any:
    """
    Log into the system.

    Generated from OpenAPI endpoint: GET /user/login

    Args:
        context: MCP context (auto-injected by framework, not user-provided)
        username: The user name for login (optional)
        password: The password for login in clear text (optional)

    Returns:
        API response (dict, list, or other JSON type)

    Example Usage:
        await logs_user_into_the_system()

        Note: 'context' parameter is auto-injected by MCP framework
    """
    # Payment already verified by @require_payment_for_tool decorator
    # No authentication required for this API - api_key not needed

    try:
        url = f"https://petstore3.swagger.io/api/v3/user/login"
        params = {
            "username": username,
            "password": password
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {}
        # No auth required for this API

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        logger.error(f"Error in logs_user_into_the_system: {e}")
        return {"error": str(e), "endpoint": "/user/login"}


@mcp.tool()
@require_payment_for_tool(
    price=TokenAmount(
        amount="10000",  # 0.01 tokens
        asset=TokenAsset(
            address="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
            decimals=6,
            network="sepolia",
            eip712=EIP712Domain(
                name="IATPWallet",
                version="1"
            )
        )
    ),
    description="Log user out of the system."

)
async def logs_out_current_logged_in_user_session(
    context: Context
) -> Any:
    """
    Log user out of the system.

    Generated from OpenAPI endpoint: GET /user/logout

    Args:
        context: MCP context (auto-injected by framework, not user-provided)


    Returns:
        API response (dict, list, or other JSON type)

    Example Usage:
        await logs_out_current_logged_in_user_session()

        Note: 'context' parameter is auto-injected by MCP framework
    """
    # Payment already verified by @require_payment_for_tool decorator
    # No authentication required for this API - api_key not needed

    try:
        url = f"https://petstore3.swagger.io/api/v3/user/logout"
        params = {}
        headers = {}
        # No auth required for this API

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        logger.error(f"Error in logs_out_current_logged_in_user_session: {e}")
        return {"error": str(e), "endpoint": "/user/logout"}


@mcp.tool()
@require_payment_for_tool(
    price=TokenAmount(
        amount="10000",  # 0.01 tokens
        asset=TokenAsset(
            address="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
            decimals=6,
            network="sepolia",
            eip712=EIP712Domain(
                name="IATPWallet",
                version="1"
            )
        )
    ),
    description="Place a new order in the store."

)
async def place_an_order_for_a_pet(
    context: Context,
    body: Dict[str, Any]
) -> Any:
    """
    Place a new order in the store.

    Generated from OpenAPI endpoint: POST /store/order

    Args:
        context: MCP context (auto-injected by framework, not user-provided)
        body: No description (optional) Examples: {}

    Returns:
        API response (dict, list, or other JSON type)

    Example Usage:
        await place_an_order_for_a_pet(body={})

        Note: 'context' parameter is auto-injected by MCP framework
    """
    # Payment already verified by @require_payment_for_tool decorator
    # No authentication required for this API - api_key not needed

    try:
        url = f"https://petstore3.swagger.io/api/v3/store/order"
        params = {}
        headers = {}
        # No auth required for this API

        response = requests.post(
            url,
            json={k: v for k, v in {
                "body": body,
            }.items() if v is not None},
            params=params,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:
        logger.error(f"Error in place_an_order_for_a_pet: {e}")
        return {"error": str(e), "endpoint": "/store/order"}


# TODO: Add your API-specific functions here

# ============================================================================
# APPLICATION SETUP WITH STARLETTE MIDDLEWARE
# ============================================================================

def create_app_with_middleware():
    """
    Create Starlette app with d402 payment middleware.
    
    Strategy:
    1. Get FastMCP's Starlette app via streamable_http_app()
    2. Extract payment configs from @require_payment_for_tool decorators
    3. Add Starlette middleware with extracted configs
    4. Single source of truth - no duplication!
    """
    logger.info("🔧 Creating FastMCP app with middleware...")
    
    # Get FastMCP's Starlette app
    app = mcp.streamable_http_app()
    logger.info(f"✅ Got FastMCP Starlette app")
    
    # Extract payment configs from decorators (single source of truth!)
    tool_payment_configs = extract_payment_configs_from_mcp(mcp, SERVER_ADDRESS)
    logger.info(f"📊 Extracted {len(tool_payment_configs)} payment configs from @require_payment_for_tool decorators")
    
    # D402 Configuration
    facilitator_url = os.getenv("FACILITATOR_URL") or os.getenv("D402_FACILITATOR_URL")
    operator_key = os.getenv("MCP_OPERATOR_PRIVATE_KEY")
    network = os.getenv("NETWORK", "sepolia")
    testing_mode = os.getenv("D402_TESTING_MODE", "false").lower() == "true"
    
    # Log D402 configuration with prominent facilitator info
    logger.info("="*60)
    logger.info("D402 Payment Protocol Configuration:")
    logger.info(f"  Server Address: {SERVER_ADDRESS}")
    logger.info(f"  Network: {network}")
    logger.info(f"  Operator Key: {'✅ Set' if operator_key else '❌ Not set'}")
    logger.info(f"  Testing Mode: {'⚠️  ENABLED (bypasses facilitator)' if testing_mode else '✅ DISABLED (uses facilitator)'}")
    logger.info("="*60)
    
    if not facilitator_url and not testing_mode:
        logger.error("❌ FACILITATOR_URL required when testing_mode is disabled!")
        raise ValueError("Set FACILITATOR_URL or enable D402_TESTING_MODE=true")
    
    if facilitator_url:
        logger.info(f"🌐 FACILITATOR: {facilitator_url}")
        if "localhost" in facilitator_url or "127.0.0.1" in facilitator_url or "host.docker.internal" in facilitator_url:
            logger.info(f"   📍 Using LOCAL facilitator for development")
        else:
            logger.info(f"   🌍 Using REMOTE facilitator for production")
    else:
        logger.warning("⚠️  D402 Testing Mode - Facilitator bypassed")
    logger.info("="*60)
    
    # Add CORS middleware first (processes before other middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods
        allow_headers=["*"],  # Allow all headers
        expose_headers=["mcp-session-id"],  # Expose custom headers to browser
    )
    logger.info("✅ Added CORS middleware (allow all origins, expose mcp-session-id)")
    
    # Add D402 payment middleware with extracted configs
    app.add_middleware(
        D402PaymentMiddleware,
        tool_payment_configs=tool_payment_configs,
        server_address=SERVER_ADDRESS,
        requires_auth=False,  # Only checks payment
        internal_api_key=None,  # No API key needed for public APIs
        testing_mode=testing_mode,
        facilitator_url=facilitator_url,
        facilitator_api_key=os.getenv("D402_FACILITATOR_API_KEY"),
        server_name="tps-1773321224-26359-mcp-server"  # MCP server ID for tracking
    )
    logger.info("✅ Added D402PaymentMiddleware")
    logger.info("   - Payment-only mode")
    
    # Add health check endpoint (bypasses middleware)
    @app.route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        """Health check endpoint for container orchestration."""
        return JSONResponse(
            content={
                "status": "healthy",
                "service": "tps-1773321224-26359-mcp-server",
                "timestamp": datetime.now().isoformat()
            }
        )
    logger.info("✅ Added /health endpoint")
    
    return app

if __name__ == "__main__":
    logger.info("="*80)
    logger.info(f"Starting TPS_1773321224_26359 MCP Server")
    logger.info("="*80)
    logger.info("Architecture:")
    logger.info("  1. D402PaymentMiddleware intercepts requests")
    logger.info("     - Checks payment → HTTP 402 if missing")
    logger.info("  2. FastMCP processes valid requests with tool decorators")
    logger.info("="*80)
    
    # Create app with middleware
    app = create_app_with_middleware()
    
    # Run with uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
