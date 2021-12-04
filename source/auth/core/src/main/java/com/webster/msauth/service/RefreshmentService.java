package com.webster.msauth.service;

import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.stereotype.Service;

import com.webster.msauth.constants.JwtExpirationConstants;
import com.webster.msauth.dto.RefreshTokenDTO;
import com.webster.msauth.dto.RefreshmentResponse;
import com.webster.msauth.exception.AuthExceptionMessage;
import com.webster.msauth.exception.InvalidRefreshTokenProvidedException;
import com.webster.msauth.models.RefreshToken;
import com.webster.msauth.repository.RefreshTokenRepository;
import com.webster.msauth.token.JwtHandle;
import com.webster.msauth.token.JwtScopeClaim;

@Service
public class RefreshmentService {
	@Autowired
	private RefreshTokenRepository refreshTokenRepository;
	@Autowired
	private JwtHandle tokenHandle;
	@Autowired
	private UserDetailsService userDetailsService;

	public RefreshmentResponse refresh(@Valid RefreshTokenDTO refreshTokenDto) {
		Optional<RefreshToken> locatedToken = refreshTokenRepository.findById(refreshTokenDto.getRefreshToken());
		if (locatedToken.isEmpty()) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.INVALID_REFRESH_TOKEN_PROVIDED;
			throw new InvalidRefreshTokenProvidedException(exceptionMessage.getErrorMessage());
		}

		RefreshToken foundToken = locatedToken.get();
		UserDetails userDetails = userDetailsService.loadUserByUsername(foundToken.getUsername());
		String accessToken = tokenHandle.createJsonWebToken(userDetails,
				JwtExpirationConstants.GENERAL_ACCESS_TOKEN_EXPIRATION_MILLISEC, JwtScopeClaim.ACCESS);

		return RefreshmentResponse.builder().accessToken(accessToken).type(JwtHandle.DEFAULT_TOKEN_TYPE)
				.subject(userDetails.getUsername()).refreshTokenExpiration(foundToken.getTimeout()).build();
	}
}
