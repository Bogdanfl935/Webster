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
import com.webster.msauth.dto.ConfirmationTokenResponse;
import com.webster.msauth.service.ConfirmationResendingService;
import com.webster.msauth.service.ConfirmationService;

@RestController
public class AccountConfirmationController {
	@Autowired
	private ConfirmationService confirmationService;
	@Autowired
	private ConfirmationResendingService confirmationResendingService;

	@PostMapping(EndpointConstants.CONFIRMATION)
	public ResponseEntity<Object> handleConfirmation(
			@RequestHeader(value = EndpointConstants.AUTHORIZATION_HEADER) String confToken) {
		confirmationService.confirm(confToken);
		return ResponseEntity.status(HttpStatus.OK).body(null);
	}

	@PostMapping(EndpointConstants.CONFIRMATION_RESENDING)
	public ResponseEntity<ConfirmationTokenResponse> handleResending(
			@Valid @RequestBody AccountNameDTO accountNameDTO) {
		ConfirmationTokenResponse resendResponse = confirmationResendingService.resend(accountNameDTO);
		return ResponseEntity.status(HttpStatus.OK).body(resendResponse);
	}
}
