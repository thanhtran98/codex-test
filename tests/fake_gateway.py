import base64, json, subprocess, sys, threading, re
from http.server import BaseHTTPRequestHandler, HTTPServer
subprocess.run("ffmpeg -y -loglevel error -f lavfi -i testsrc=duration=3:size=1280x720:rate=24 -pix_fmt yuv420p fake.mp4",shell=True,check=True)
subprocess.run("ffmpeg -y -loglevel error -f lavfi -i sine=frequency=440:duration=3 fake.mp3",shell=True,check=True)
PNG=base64.b64encode(open('/dev/null','rb').read() or bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d49444154789c6360000002000001e221bc330000000049454e44ae426082")).decode()
STATE={"video_posts":0,"polls":0,"file_ok":[]}
class H(BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def send(self,code,body,ct="application/json",extra=None):
        b=body if isinstance(body,bytes) else json.dumps(body).encode()
        self.send_response(code);self.send_header("Content-Type",ct)
        for k,v in (extra or {}).items():self.send_header(k,v)
        self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
    def body(self):
        n=int(self.headers.get("Content-Length",0));return self.rfile.read(n)
    def do_GET(self):
        if self.headers.get("Authorization")!="Bearer TESTKEY":return self.send(401,{"error":"bad key"})
        p=self.path.split("?")[0]
        if p=="/v1/models":return self.send(200,{"data":[]})
        if p=="/key/info":return self.send(200,{"info":{"spend":0.12,"team_id":"T1"}})
        if p=="/team/info":return self.send(200,{"team_info":{"spend":0.3,"max_budget":1}})
        m=re.match(r"/v1/videos/(\w+)(/content)?$",p)
        if m and m.group(2):return self.send(200,open("fake.mp4","rb").read(),"video/mp4",{"x-litellm-response-cost":"0.2"} if False else None)
        if m:
            STATE["polls"]+=1
            return self.send(200,{"id":m.group(1),"status":"processing" if STATE["polls"]<2 else "completed"})
        self.send(404,{"error":"nf"})
    def do_POST(self):
        if self.headers.get("Authorization")!="Bearer TESTKEY":return self.send(401,{"error":"bad key"})
        raw=self.body();p=self.path
        if p=="/v1/audio/speech":return self.send(404,{"error":"use /audio/speech"})
        if p=="/audio/speech":return self.send(200,open("fake.mp3","rb").read(),"audio/mpeg")
        if b"BUDGET" in raw:return self.send(429,{"error":"Budget has been exceeded"})
        if p=="/v1/images/generations":
            j=json.loads(raw);STATE["last_img"]=j
            return self.send(200,{"data":[{"b64_json":PNG}]},extra={"x-litellm-response-cost":"0.0336"})
        if p=="/v1/chat/completions":
            j=json.loads(raw);c=j["messages"][0]["content"]
            if j.get("tools"):return self.send(200,{"choices":[{"message":{"content":"Kết quả có nguồn: A"}}]})
            if isinstance(c,list) and "nano" in j["model"]:
                return self.send(200,{"choices":[{"message":{"content":"","images":[{"image_url":{"url":"data:image/png;base64,"+PNG}}]}}]})
            return self.send(200,{"choices":[{"message":{"content":"Chữ: ĐỘI MŨ BẢO HIỂM. Không lỗi dấu."}}]})
        if p=="/v1/videos":
            STATE["video_posts"]+=1
            ok=b"PNGDATA123" in raw if b"multipart" in self.headers.get("Content-Type","").encode() else None
            STATE["file_ok"].append((STATE["video_posts"],ok))
            if STATE["video_posts"]==1:return self.send(429,{"error":"rate limit"})
            open("state.json","w").write(json.dumps(STATE))
            return self.send(200,{"id":"video_abc","status":"processing"})
        self.send(404,{"error":"nf "+p})
HTTPServer(("127.0.0.1",8765),H).serve_forever()
