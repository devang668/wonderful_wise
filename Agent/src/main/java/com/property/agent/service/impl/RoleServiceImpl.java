package com.property.agent.service.impl;

import com.property.agent.model.Role;
import com.property.agent.service.RoleService;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * 角色服务实现类
 */
@Service
public class RoleServiceImpl implements RoleService {
    
    // 使用HashMap作为内存存储
    private final Map<String, Role> roleMap = new HashMap<>();
    
    @Override
    public List<Role> getAllRoles() {
        return new ArrayList<>(roleMap.values());
    }
    
    @Override
    public Role getRoleById(String roleId) {
        return roleMap.get(roleId);
    }
    
    @Override
    public List<Role> searchRoles(String keyword) {
        if (keyword == null || keyword.trim().isEmpty()) {
            return getAllRoles();
        }
        
        List<Role> result = new ArrayList<>();
        String lowerKeyword = keyword.toLowerCase();
        
        for (Role role : roleMap.values()) {
            if (role.getName().toLowerCase().contains(lowerKeyword) ||
                role.getDescription().toLowerCase().contains(lowerKeyword) ||
                role.getSkills().toLowerCase().contains(lowerKeyword)) {
                result.add(role);
            }
        }
        
        return result;
    }
    
    @Override
    public List<Role> getRolesByType(String type) {
        if (type == null || type.trim().isEmpty()) {
            return getAllRoles();
        }
        
        List<Role> result = new ArrayList<>();
        for (Role role : roleMap.values()) {
            if (type.equals(role.getType())) {
                result.add(role);
            }
        }
        
        return result;
    }
    
    @Override
    public String generateRolePrompt(String roleId, Map<String, String> additionalInfo) {
        Role role = getRoleById(roleId);
        if (role == null) {
            return "你是一个AI助手，可以回答用户的问题。";
        }
        
        String prompt = role.getPromptTemplate();
        
        // 填充额外信息
        if (additionalInfo != null) {
            for (Map.Entry<String, String> entry : additionalInfo.entrySet()) {
                prompt = prompt.replace("{" + entry.getKey() + "}", entry.getValue());
            }
        }
        
        return prompt;
    }
    
    @Override
    public void initRoleData() {
        // 检查是否已有角色数据
        if (roleMap.isEmpty()) {
            // 初始化三个AI角色
            
            // 1. 爱因斯坦角色 - 科学家
            Role einstein = new Role();
            einstein.setId("einstein");
            einstein.setName("爱因斯坦");
            einstein.setDescription("著名物理学家，相对论的创立者，拥有丰富的科学知识。");
            einstein.setPromptTemplate("你是阿尔伯特·爱因斯坦，20世纪最伟大的物理学家之一，相对论的创立者。你说话简洁明了，善于用通俗易懂的方式解释复杂的科学概念。你的性格温和、好奇、富有智慧。请以爱因斯坦的身份回答用户的问题，保持科学严谨性的同时尽量用简单易懂的语言。");
            einstein.setAvatar("https://picsum.photos/seed/einstein/100/100");
            einstein.setType("scientist");
            einstein.setSkills("科学知识讲解，相对论解释，物理概念普及，科学思维训练");
            roleMap.put(einstein.getId(), einstein);
            
            // 2. 哈利·波特角色 - 虚构人物
            Role harryPotter = new Role();
            harryPotter.setId("harry-potter");
            harryPotter.setName("哈利·波特");
            harryPotter.setDescription("《哈利波特》系列小说的主角，霍格沃茨魔法学校的学生，擅长魁地奇和黑魔法防御术。");
            harryPotter.setPromptTemplate("你是哈利·波特，霍格沃茨魔法学校的学生，著名的'大难不死的男孩'。你经历过许多冒险，对抗过伏地魔。你的性格勇敢、忠诚、富有正义感。请以哈利·波特的身份回答用户的问题，使用魔法世界的术语，分享你的冒险经历和对魔法的理解。");
            harryPotter.setAvatar("https://picsum.photos/seed/harry/100/100");
            harryPotter.setType("fictional");
            harryPotter.setSkills("魔法知识讲解，冒险故事分享，魁地奇介绍，黑魔法防御术指导");
            roleMap.put(harryPotter.getId(), harryPotter);
            
            // 3. 苏格拉底角色 - 哲学家
            Role socrates = new Role();
            socrates.setId("socrates");
            socrates.setName("苏格拉底");
            socrates.setDescription("古希腊著名哲学家，西方哲学的奠基人之一，以对话法和苏格拉底式提问闻名。");
            socrates.setPromptTemplate("你是苏格拉底，古希腊著名的哲学家，西方哲学的奠基人之一。你擅长使用对话法引导他人思考，通过提问帮助人们发现自己的无知并追求真理。你的性格温和而坚定，充满智慧。请以苏格拉底的身份回答用户的问题，尽量使用提问的方式引导用户思考，而不是直接给出答案。");
            socrates.setAvatar("https://picsum.photos/seed/socrates/100/100");
            socrates.setType("philosopher");
            socrates.setSkills("哲学思考引导，苏格拉底式提问，伦理道德探讨，逻辑思维训练");
            roleMap.put(socrates.getId(), socrates);
        }
    }
    
    @Override
    public Role createRole(Role role) {
        // 生成唯一ID
        if (role.getId() == null || role.getId().isEmpty()) {
            role.setId(UUID.randomUUID().toString().replace("-", ""));
        }
        
        // 设置默认头像
        if (role.getAvatar() == null || role.getAvatar().isEmpty()) {
            role.setAvatar("https://picsum.photos/seed/" + role.getId() + "/100/100");
        }
        
        // 保存到内存
        roleMap.put(role.getId(), role);
        
        return role;
    }
}