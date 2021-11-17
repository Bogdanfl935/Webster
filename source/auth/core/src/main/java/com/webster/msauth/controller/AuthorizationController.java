package com.webster.msauth.controller;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
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

@RestController
public class AuthorizationController {
	@Autowired
	private AuthorizationService authorizationService;
	@Autowired
	private RefreshmentService refreshmentService;

	@PostMapping(EndpointConstants.AUTHORIZATION)
	public ResponseEntity<AuthorizationResponse> handleAuthorization(
			@RequestHeader(value = EndpointConstants.AUTHORIZATION_HEADER) String authToken) {
		AuthorizationResponse authorizationResponse = authorizationService.validate(authToken);
		return ResponseEntity.status(HttpStatus.OK).body(authorizationResponse);
	}

	@PostMapping(EndpointConstants.REFRESHMENT)
	public ResponseEntity<RefreshmentResponse> handleRefreshment(@Valid @RequestBody RefreshTokenDTO refreshTokenDto) {
		RefreshmentResponse refreshmentResponse = refreshmentService.refresh(refreshTokenDto);
		return ResponseEntity.status(HttpStatus.OK).body(refreshmentResponse);
	}
}
