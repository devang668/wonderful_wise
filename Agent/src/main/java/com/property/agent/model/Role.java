package com.property.agent.model;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

/**
 * AI角色实体类
 */
@Data
@TableName("role")
public class Role {
    /**
     * 角色ID
     */
    private String id;
    
    /**
     * 角色名称
     */
    private String name;
    
    /**
     * 角色描述
     */
    private String description;
    
    /**
     * 角色提示词模板
     */
    @TableField("prompt_template")
    private String promptTemplate;
    
    /**
     * 角色头像URL
     */
    private String avatar;
    
    /**
     * 角色类型
     */
    private String type;
    
    /**
     * 角色技能描述
     */
    private String skills;
}