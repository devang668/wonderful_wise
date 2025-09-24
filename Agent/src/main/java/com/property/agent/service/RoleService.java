package com.property.agent.service;

import com.property.agent.model.Role;
import java.util.List;
import java.util.Map;

/**
 * 角色服务接口
 */
public interface RoleService {
    
    /**
     * 获取所有角色
     * @return 角色列表
     */
    List<Role> getAllRoles();
    
    /**
     * 根据ID获取角色
     * @param roleId 角色ID
     * @return 角色对象
     */
    Role getRoleById(String roleId);
    
    /**
     * 搜索角色
     * @param keyword 搜索关键词
     * @return 匹配的角色列表
     */
    List<Role> searchRoles(String keyword);
    
    /**
     * 根据类型获取角色
     * @param type 角色类型
     * @return 匹配的角色列表
     */
    List<Role> getRolesByType(String type);
    
    /**
     * 获取角色提示词
     * @param roleId 角色ID
     * @param additionalInfo 额外信息（可选）
     * @return 生成的提示词
     */
    String generateRolePrompt(String roleId, Map<String, String> additionalInfo);
    
    /**
     * 初始化角色数据
     */
    void initRoleData();
    
    /**
     * 创建新角色
     * @param role 角色对象
     * @return 创建的角色
     */
    Role createRole(Role role);
}