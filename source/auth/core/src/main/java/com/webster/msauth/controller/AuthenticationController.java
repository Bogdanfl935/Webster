package com.webster.msauth.controller;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.webster.msauth.constants.EndpointConstants;
import com.webster.msauth.dto.AuthenticationResponse;
import com.webster.msauth.dto.ConfirmationTokenResponse;
import com.webster.msauth.dto.LoginUserDTO;
import com.webster.msauth.dto.RegisterUserDTO;
import com.webster.msauth.service.AuthenticationService;
import com.webster.msauth.service.RegistrationService;

@RestController
public class AuthenticationController {
	@Autowired
	private RegistrationService registrationService;
	@Autowired
	private AuthenticationService authenticationService;

	@PostMapping(EndpointConstants.REGISTRATION)
	public ResponseEntity<ConfirmationTokenResponse> handleRegistration(
			@Valid @RequestBody RegisterUserDTO registerUserDto) {
		ConfirmationTokenResponse registrationResponse = registrationService.register(registerUserDto);
		return ResponseEntity.status(HttpStatus.CREATED).body(registrationResponse);
	}

	@PostMapping(EndpointConstants.AUTHENTICATION)
	public ResponseEntity<AuthenticationResponse> handleAuthentication(@Valid @RequestBody LoginUserDTO loginUserDto) {
		AuthenticationResponse authenticationResponse = authenticationService.login(loginUserDto);
		return ResponseEntity.status(HttpStatus.OK).body(authenticationResponse);
	}
}
