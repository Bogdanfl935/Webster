package com.webster.msauth.configurer;

import org.springframework.context.annotation.Configuration;
import org.springframework.format.FormatterRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import com.webster.msauth.service.StringToJwtScopeClaimConverter;

@Configuration
public class FormattersWebConfig implements WebMvcConfigurer {
    @Override
    public void addFormatters(FormatterRegistry registry) {
        registry.addConverter(new StringToJwtScopeClaimConverter());
    }
}