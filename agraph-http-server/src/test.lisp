(in-package :agraph-http-server)

(setf *server* (make-instance 'agraph-http-server :cache-file "/home/marijn/src/lisp/agraph-http-server/data"))
(start :port 8080)
(publish-http-server *wserver* *server*)

(net.aserve::debug-on :notrap)
(setf net.aserve::*enable-logging* nil)