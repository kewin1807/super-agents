from typing import Dict, Any
import httpx
FIREANT_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxODg5NjIyNTMwLCJuYmYiOjE1ODk2MjI1MzAsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsiYWNhZGVteS1yZWFkIiwiYWNhZGVteS13cml0ZSIsImFjY291bnRzLXJlYWQiLCJhY2NvdW50cy13cml0ZSIsImJsb2ctcmVhZCIsImNvbXBhbmllcy1yZWFkIiwiZmluYW5jZS1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImludmVzdG9wZWRpYS1yZWFkIiwib3JkZXJzLXJlYWQiLCJvcmRlcnMtd3JpdGUiLCJwb3N0cy1yZWFkIiwicG9zdHMtd3JpdGUiLCJzZWFyY2giLCJzeW1ib2xzLXJlYWQiLCJ1c2VyLWRhdGEtcmVhZCIsInVzZXItZGF0YS13cml0ZSIsInVzZXJzLXJlYWQiXSwianRpIjoiMjYxYTZhYWQ2MTQ5Njk1ZmJiYzcwODM5MjM0Njc1NWQifQ.dA5-HVzWv-BRfEiAd24uNBiBxASO-PAyWeWESovZm_hj4aXMAZA1-bWNZeXt88dqogo18AwpDQ-h6gefLPdZSFrG5umC1dVWaeYvUnGm62g4XS29fj6p01dhKNNqrsu5KrhnhdnKYVv9VdmbmqDfWR8wDgglk5cJFqalzq6dJWJInFQEPmUs9BW_Zs8tQDn-i5r4tYq2U8vCdqptXoM7YgPllXaPVDeccC9QNu2Xlp9WUvoROzoQXg25lFub1IYkTrM66gJ6t9fJRZToewCt495WNEOQFa_rwLCZ1QwzvL0iYkONHS_jZ0BOhBCdW9dWSawD6iF1SIQaFROvMDH1rg"


async def handle_response_fireant(api_key: str, endpoint: str, query: Dict[str, Any]):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.fireant.vn{endpoint}", headers={"Authorization": f"Bearer {api_key}"}, params=query)
        return response.json()


class FireantService:
    def __init__(self):
        self.fireant_api_key = ""

    async def initialize_api_key(self):
        # Assuming these utility functions are defined elsewhere
        api_key = FIREANT_API_KEY
        if api_key:
            self.fireant_api_key = api_key

    def get_fireant_api_key(self):
        return self.fireant_api_key

    async def get_list_official_post_vn_stock(self, query: Dict[str, Any]):
        """
        Get list official post of a VN stock ticker
        {
            "symbol": z.string().describe("The stock symbol, e.g: VNM, FPT, VIC"),
            "offset": z.number().describe("The offset value, default is 0"),
            "limit": z.number().describe("The number of records to return, default is 10")
        }
        """
        response = await handle_response_fireant(self.fireant_api_key, "/posts?type=1", query)
        print("getListOfficialPostVnStock", response)
        return response

    async def get_list_user_post_vn_stock(self, query: Dict[str, Any]):
        response = await handle_response_fireant(self.fireant_api_key, "/posts?type=0", query)
        print("getListUserPostVnStock", response)
        return response

    # Get information of each ticker
    async def get_fundamental_analysis_ticker_vn_stock(self, symbol: str):
        """
        Get fundamental analysis of a ticker
        symbol: str
        """
        response = await handle_response_fireant(self.fireant_api_key, f"/symbols/{symbol}/fundamental", {})
        print("getFundamentalAnalysisTickerVnStock", response)
        return response

    async def get_profile_vn_stock(self, symbol: str):
        """
        Get profile company of a ticker
        symbol: str
        """
        response = await handle_response_fireant(self.fireant_api_key, f"/symbols/{symbol}/profile", {})
        print("getProfileVnStock", response)
        return response

    async def get_holder_of_ticker_vn_stock(self, symbol: str):
        """
        Get holder of a VN stock ticker
        symbol: str
        """
        response = await handle_response_fireant(self.fireant_api_key, f"/symbols/{symbol}/holders", {})
        print("getHolderofTickerVnStock", response)
        return response

    async def get_history_price_vn_stock(self, query: Dict[str, Any]):
        """
        Get history price of a VN stock ticker like OHLC data
        {
            "symbol": z.string().describe("The stock symbol, e.g: VNM, FPT, VIC"),
            "startDate": z.string().describe("The start date in YYYY-MM-DD format, default is 1 week ago"),
            "endDate": z.string().describe("The end date in YYYY-MM-DD format, default is today"),
            "offset": z.number().describe("The offset value, default is 0"),
            "limit": z.number().describe("The number of records to return, default is 100")
        }
        """
        response = await handle_response_fireant(
            self.fireant_api_key,
            f"/symbols/{query['symbol']}/historical-quotes",
            query
        )
        print("getHistoryPriceVnStock", response)
        return response

    async def get_financial_statement_vn_stock(self, query: Dict[str, Any]):
        """
        Get financial statement of a VN stock ticker
        {
            "symbol": z.string().describe("The stock symbol, e.g: VNM, FPT, VIC"),
            "type": z.enum(Object.values(EFinancialStatementPeriod) as [string, ...string[]]).describe("Financial statement period: 'Q' (quarterly) or 'Y' (yearly)"),
            "count": z.number().describe("The number of records to return, default is 10")
        }
        """
        response = await handle_response_fireant(
            self.fireant_api_key,
            f"/symbols/{query['symbol']}/financial-data",
            query
        )
        print("getFinancialStatementVnStock", response)
        return response


# Create singleton instance
fireant_service = FireantService()
