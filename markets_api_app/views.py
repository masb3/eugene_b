from rest_framework.response import Response
from rest_framework.views import APIView

from .dadata_utils import get_dadata_clean_address, get_lat_lon, get_3km_market


class MarketApiView(APIView):
    def get(self, request, *args, **kwargs):
        addr = request.query_params.get('address')
        if not addr:
            return Response({'Error': 'Incorrect querystring'}, status=400)

        data = ('["%s"]' % addr).encode('utf-8')
        resp = get_dadata_clean_address(data)
        if 200 == resp.status_code:
            lat_lon = get_lat_lon(resp.json()[0])
            if lat_lon:
                resp = get_3km_market(latitude=float(lat_lon['latitude']), longitude=float(lat_lon['longitude']))
                return Response(resp)
            return Response({'Error': 'Unable to get latitude & longitude'}, status=400)
        return Response(resp.json(), status=resp.status_code)
