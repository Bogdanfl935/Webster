package com.webster.msauth.controller;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import com.webster.msauth.constants.EndpointConstants;
import com.webster.msauth.dto.AuthorizationResponse;
import com.webster.msauth.dto.RefreshTokenDTO;
import com.webster.msauth.dto.RefreshmentResponse;
import com.webster.msauth.service.AuthorizationService;
import com.webster.msauth.service.RefreshmentService;
import com.webster.msauth.token.JwtScopeClaim;

@RestController
public class AuthorizationController {
	@Autowired
	private AuthorizationService authorizationService;
	@Autowired
	private RefreshmentService refreshmentService;

	@PostMapping(EndpointConstants.AUTHORIZATION + "/{" + JwtScopeClaim.SCOPE_CLAIM + "}")
	public ResponseEntity<AuthorizationResponse> handleAuthorization(
			@PathVariable(JwtScopeClaim.SCOPE_CLAIM) JwtScopeClaim scope,
			@RequestHeader(value = EndpointConstants.AUTHORIZATION_HEADER) String authToken) {
		AuthorizationResponse authorizationResponse = authorizationService.validate(authToken, scope);
		return ResponseEntity.status(HttpStatus.OK).body(authorizationResponse);
	}

	@PostMapping(EndpointConstants.REFRESHMENT)
	public ResponseEntity<RefreshmentResponse> handleRefreshment(@Valid @RequestBody RefreshTokenDTO refreshTokenDto) {
		RefreshmentResponse refreshmentResponse = refreshmentService.refresh(refreshTokenDto);
		return ResponseEntity.status(HttpStatus.OK).body(refreshmentResponse);
	}
}
