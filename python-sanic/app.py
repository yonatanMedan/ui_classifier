from sanic import Sanic
from sanic.response import json

app = Sanic()

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

@app.route('/train',methods=["POST",])
async def train(request):
  return json({"req_body":request.json})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
