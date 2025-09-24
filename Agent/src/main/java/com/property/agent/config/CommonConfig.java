package com.property.agent.config;

import com.property.agent.aiservice.ConsultantService;
import com.property.agent.repository.RedisChatMemoryStore;
import dev.langchain4j.data.document.Document;

import dev.langchain4j.memory.ChatMemory;
import dev.langchain4j.memory.chat.ChatMemoryProvider;
import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.rag.content.retriever.ContentRetriever;
import dev.langchain4j.rag.content.retriever.EmbeddingStoreContentRetriever;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.store.embedding.EmbeddingStore;
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor;
import dev.langchain4j.store.embedding.inmemory.InMemoryEmbeddingStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.core.StringRedisTemplate;

import java.util.List;

@Configuration
public class CommonConfig {

    @Autowired
    private OpenAiChatModel model;
    @Autowired
    private RedisChatMemoryStore redisChatMemoryStore;
    @Autowired
    private EmbeddingModel embeddingModel;

    @Bean
    public ChatMemoryProvider chatMemoryProvider(){
        ChatMemoryProvider chatMemoryProvider = new ChatMemoryProvider() {
            @Override
            public ChatMemory get(Object memoryId) {
                return MessageWindowChatMemory.builder()
                        .id(memoryId)
                        .maxMessages(20)
                        .chatMemoryStore(redisChatMemoryStore)
                        .build();
            }
        };
        return chatMemoryProvider;
    }
//    // 构建向量数据库对象
//    @Bean
//    public EmbeddingStore store() {
//        // 加载数据进入内存
//        List<Document> content = ClassPathDocumentLoader.loadDocuments("content");
//        // 构建向量数据库操作对象
//        InMemoryEmbeddingStore store = new InMemoryEmbeddingStore();
//        // 构建数据处理和存储工具
//        EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor.builder()
//                .embeddingStore(store)
//                .embeddingModel(embeddingModel)
//                .build();
//        ingestor.ingest(content);
//        return store;
//    }
//
//    // 构建向量对象检索对象（通过参数注入获取store实例）
//    @Bean
//    public ContentRetriever contentRetriever(EmbeddingStore store) {  // 这里通过参数注入
//        return EmbeddingStoreContentRetriever.builder()
//                .embeddingStore(store)  // 使用注入的store实例
//                .minScore(0.6)
//                .embeddingModel(embeddingModel)
//                .maxResults(3)
//                .build();
//    }

//    @Bean
//    public ConsultantService consultantService(){
//        ConsultantService consultantService = AiServices.builder(ConsultantService.class)
//                .chatLanguageModel(model)
//                .build();
//        return consultantService;
//    }
}