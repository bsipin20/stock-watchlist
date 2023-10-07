from flask import jsonify

def health():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

ROUTES = {
    '/v1/health': (health, ['GET'])
}
