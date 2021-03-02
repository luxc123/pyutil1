package com.robot.epc.base.config;

import com.robot.epc.base.dao.DictMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import javax.websocket.*;
import javax.websocket.server.PathParam;
import javax.websocket.server.ServerEndpoint;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@ServerEndpoint("/webSocket/{username}")
@Slf4j
@Component
public class MyWebSocket {

    private static int onlineCount = 0;
    public static Map<String, MyWebSocket> clients = new ConcurrentHashMap<String, MyWebSocket>();
    public Session session;
    private String username;

    @Autowired
    private DictMapper dictMapper;

    @OnOpen
    public void onOpen(@PathParam("username") String username, Session session) {
        this.username = username;
        this.session = session;
        MyWebSocket.onlineCount++;
        clients.put(username, this);
    }

    @OnClose
    public void onClose() {
        clients.remove(username);
        MyWebSocket.onlineCount--;
    }

    @OnMessage
    public void onMessage(String message) {}

    @OnError
    public void onError(Session session, Throwable throwable) {
        log.error("WebSocket发生错误：" + throwable.getMessage());
    }

    @Scheduled(cron="0/3 * * * * *")
    public void sendMessage() {
        // 向所有连接websocket的客户端发送消息
        // 可以修改为对某个客户端发消息
//        List<DictEntity> all = dictMapper.getAll(new DictDTO());
        for (MyWebSocket item : clients.values()) {
            item.session.getAsyncRemote().sendText("测试!!@123");
//            item.session.getAsyncRemote().sendObject(all);
        }
    }

}

