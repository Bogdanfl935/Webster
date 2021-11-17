package com.webster.msauth.token;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.webster.msauth.constants.ExternConfigConstants;
import com.webster.msauth.constants.ExternConfigValidationConstants;

import lombok.Getter;

@Component
public class JwtConfig {
	@Value(ExternConfigConstants.TOKEN_CONFIG_JWT_ISSUER)
	@NotNull
	@Getter
	@Size(max = ExternConfigValidationConstants.ISSUER_MAX_LENGTH)
	private String tokenIssuer;
}
