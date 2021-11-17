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
import com.webster.msauth.dto.AccountNameDTO;
import com.webster.msauth.dto.ForgottenPasswordResponse;
import com.webster.msauth.dto.PasswordResetDTO;
import com.webster.msauth.service.ForgottenPasswordService;
import com.webster.msauth.service.PasswordResetService;

@RestController
public class PasswordResetController {
	@Autowired
	private ForgottenPasswordService forgottenPasswordService;
	@Autowired
	private PasswordResetService passwordResetService;

	@PostMapping(EndpointConstants.PASSWORD_RESETTING)
	public ResponseEntity<ForgottenPasswordResponse> handlePasswordResetting(
			@Valid @RequestBody PasswordResetDTO passwordResetDTO,
			@RequestHeader(value = EndpointConstants.AUTHORIZATION_HEADER) String resetToken) {
		passwordResetService.reset(passwordResetDTO, resetToken);
		return ResponseEntity.status(HttpStatus.OK).body(null);
	}

	@PostMapping(EndpointConstants.PASSWORD_FORGOTTEN)
	public ResponseEntity<ForgottenPasswordResponse> handleForgottenPassword(
			@Valid @RequestBody AccountNameDTO accountNameDTO) {
		ForgottenPasswordResponse forgottenPasswordResponse = forgottenPasswordService.createResetToken(accountNameDTO);
		return ResponseEntity.status(HttpStatus.OK).body(forgottenPasswordResponse);
	}
}
