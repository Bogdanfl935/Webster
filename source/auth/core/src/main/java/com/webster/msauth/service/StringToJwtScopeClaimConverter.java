package com.webster.msauth.service;

import java.util.NoSuchElementException;

import org.springframework.core.convert.converter.Converter;

import com.webster.msauth.exception.JwtScopeClaimConversionFailException;
import com.webster.msauth.token.JwtScopeClaim;

public class StringToJwtScopeClaimConverter implements Converter<String, JwtScopeClaim> {

	@Override
	public JwtScopeClaim convert(String source) {
		JwtScopeClaim scopeClaim = null;
		try {
			scopeClaim = JwtScopeClaim.getAssociatedScope(source);
		} catch (NoSuchElementException exception) {
			throw new JwtScopeClaimConversionFailException();
		}
		return scopeClaim;
	}

}
