    // 与websocket服务器创建连接
    createWebSocket() {
      // 注意这里的端口号是后端服务的端口号，后面的是后端正常请求的路径，base是我的项目名，最后面的是我放在cookie中的当前登陆用户
      let websocket = new WebSocket('ws://127.0.0.1:8088/base/webSocket/luxc' )
      // 连接成功时
      websocket.onopen = () => {
        websocket.send('hello')
      }
      websocket.onmessage = event => {
        // 后端发送的消息在event.data中
        console.log(event.data)
      }
      websocket.onclose = function () {
        console.log('关闭了')
      }
      // 路由跳转时结束websocket链接
      this.$router.afterEach(function () {
        websocket.close()
      })
      // 监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常
      window.onbeforeunload = function () {
        websocket.close()
      }
    }