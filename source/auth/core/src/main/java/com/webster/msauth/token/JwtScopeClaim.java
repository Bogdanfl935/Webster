package com.webster.msauth.token;

import java.util.Arrays;

import javax.validation.constraints.NotNull;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum JwtScopeClaim {
	ACCESS("access"), CONFIRM("confirm"), RESET("reset");

	@Getter
	@NotNull
	private String scope;
	public static final String SCOPE_CLAIM = "scope";

	public static JwtScopeClaim getAssociatedScope(String scope) {
		return Arrays.asList(JwtScopeClaim.values()).stream()
				.filter(scopeClaim -> scopeClaim.getScope().equalsIgnoreCase(scope)).findFirst().orElseThrow();
	}
}
