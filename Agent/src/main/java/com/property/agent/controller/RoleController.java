package com.property.agent.controller;

import com.property.agent.model.Role;
import com.property.agent.service.RoleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 角色控制器
 */
@RestController
@RequestMapping("/roles")
public class RoleController {
    
    @Autowired
    private RoleService roleService;
    
    /**
     * 获取所有角色
     */
    @GetMapping
    public List<Role> getAllRoles() {
        return roleService.getAllRoles();
    }
    
    /**
     * 根据ID获取角色详情
     */
    @GetMapping("/{roleId}")
    public Role getRoleById(@PathVariable String roleId) {
        return roleService.getRoleById(roleId);
    }
    
    /**
     * 搜索角色
     */
    @GetMapping("/search")
    public List<Role> searchRoles(@RequestParam String keyword) {
        return roleService.searchRoles(keyword);
    }
    
    /**
     * 根据类型获取角色
     */
    @GetMapping("/type/{type}")
    public List<Role> getRolesByType(@PathVariable String type) {
        return roleService.getRolesByType(type);
    }
    
    /**
     * 获取角色提示词
     */
    @PostMapping("/{roleId}/prompt")
    public String generateRolePrompt(@PathVariable String roleId, @RequestBody(required = false) Map<String, String> additionalInfo) {
        return roleService.generateRolePrompt(roleId, additionalInfo);
    }
    
    /**
     * 初始化角色数据
     */
    @PostMapping("/init")
    public String initRoleData() {
        roleService.initRoleData();
        return "角色数据初始化成功";
    }
    
    /**
     * 创建新角色
     */
    @PostMapping
    public Role createRole(@RequestBody Role role) {
        return roleService.createRole(role);
    }
}