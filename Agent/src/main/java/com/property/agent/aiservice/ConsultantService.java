package com.property.agent.aiservice;

import dev.langchain4j.service.MemoryId;
import dev.langchain4j.service.UserMessage;
import dev.langchain4j.service.spring.AiService;
import dev.langchain4j.service.spring.AiServiceWiringMode;
import org.springframework.context.annotation.Configuration;

@AiService(
        wiringMode = AiServiceWiringMode.EXPLICIT, // 手动装配
        chatModel = "openAiChatModel", // 指定模型
        streamingChatModel = "openAiStreamingChatModel",
        chatMemoryProvider = "chatMemoryProvider"//配置会话记忆提供者对象

        //contentRetriever = "contentRetriever"//配置向量数据库检索对象
)
//@AiService
public interface ConsultantService {
     // 用于聊天的方法
     // public String chat(String message);
     String chat(@MemoryId String memoryId, @UserMessage String message);
}