package com.property.agent.config;

import com.property.agent.service.RoleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

/**
 * 应用初始化配置类
 * 用于在应用启动时执行一些初始化操作
 */
@Component
public class InitConfig implements ApplicationRunner {
    
    @Autowired
    private RoleService roleService;
    
    @Override
    public void run(ApplicationArguments args) throws Exception {
        // 初始化角色数据
        roleService.initRoleData();
        System.out.println("角色数据初始化完成");
    }
}