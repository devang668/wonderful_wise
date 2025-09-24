package com.property.agent.controller;

import com.property.agent.aiservice.ConsultantService;
import com.property.agent.service.RoleService;
import dev.langchain4j.memory.chat.ChatMemoryProvider;
import dev.langchain4j.model.chat.StreamingChatLanguageModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;



@Controller
public class ChatController {

    @Autowired
    private ConsultantService consultantService;

    @Autowired
    private RoleService roleService;

    @Autowired
    private StreamingChatLanguageModel streamingChatLanguageModel;

    @Autowired
    private ChatMemoryProvider chatMemoryProvider; // 注入对话记忆提供者

    @RequestMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter chat(
            @RequestParam String memoryId,
            @RequestParam String message,
            @RequestParam(required = false) String roleId) {

        SseEmitter emitter = new SseEmitter(1800000L); // 30分钟超时

        if (roleId != null && !roleId.isEmpty()) {
            // 角色对话分支：使用ConsultantService进行非流式调用
            try {
                String response = consultantService.chat(memoryId, message);
                emitter.send(response);
                emitter.complete();
            } catch (Exception e) {
                try {
                    emitter.completeWithError(e);
                } catch (Exception ignored) {
                    // 忽略异常，连接可能已关闭
                }
            }
        } else {
            // 默认分支：非流式调用ConsultantService
            try {
                String response = consultantService.chat(memoryId, message);
                emitter.send(response);
                emitter.complete();
            } catch (Exception e) {
                try {
                    emitter.completeWithError(e);
                } catch (Exception ignored) {
                    // 忽略异常，连接可能已关闭
                }
            }
        }

        return emitter;
    }
}