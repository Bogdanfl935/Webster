package com.webster.msauth.service;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.CredentialsExpiredException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.stereotype.Service;

import com.webster.msauth.constants.JwtExpirationConstants;
import com.webster.msauth.dto.AuthenticationResponse;
import com.webster.msauth.dto.LoginUserDTO;
import com.webster.msauth.exception.AccountNotConfirmedException;
import com.webster.msauth.exception.AuthExceptionMessage;
import com.webster.msauth.exception.InvalidUsernameOrPasswordException;
import com.webster.msauth.models.RefreshToken;
import com.webster.msauth.repository.RefreshTokenRepository;
import com.webster.msauth.token.JwtHandle;
import com.webster.msauth.token.OpaqueTokenHandle;

@Service
public class AuthenticationService {
	@Autowired
	private UserDetailsService userDetailsService;
	@Autowired
	private AuthenticationManager authenticationManager;
	@Autowired
	private JwtHandle jwtHandle;
	@Autowired
	private OpaqueTokenHandle refHandle;
	@Autowired
	private RefreshTokenRepository refreshTokenRepository;

	public AuthenticationResponse login(@Valid LoginUserDTO loginUserDto) {
		try {
			authenticationManager.authenticate(
					new UsernamePasswordAuthenticationToken(loginUserDto.getUsername(), loginUserDto.getPassword()));
		}
		catch (BadCredentialsException exception) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.INVALID_USERNAME_OR_PASSWORD;
			throw new InvalidUsernameOrPasswordException(exceptionMessage.getErrorMessage());
		}
		catch (CredentialsExpiredException exception) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.ACCOUNT_NOT_CONFIRMED;
			exceptionMessage.setErrorParameter(loginUserDto.getUsername());
			throw new AccountNotConfirmedException(exceptionMessage.getErrorMessage());
		}
		catch (AuthenticationException exception) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.INVALID_USERNAME_OR_PASSWORD;
			throw new InvalidUsernameOrPasswordException(exceptionMessage.getErrorMessage());
		}

		UserDetails userDetails = userDetailsService.loadUserByUsername(loginUserDto.getUsername());

		String accessToken = jwtHandle.createJsonWebToken(userDetails,
				JwtExpirationConstants.GENERAL_ACCESS_TOKEN_EXPIRATION_MILLISEC);
		String refreshToken = refHandle.createRefreshToken();

		/* Save user-refreshToken pair in Redis cache */
		refreshTokenRepository.save(new RefreshToken(refreshToken, userDetails.getUsername()));

		return new AuthenticationResponse(accessToken, refreshToken, JwtHandle.DEFAULT_TOKEN_TYPE);
	}
}
