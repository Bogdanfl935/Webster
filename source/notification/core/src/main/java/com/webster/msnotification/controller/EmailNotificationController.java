package com.webster.msnotification.controller;

import javax.validation.Valid;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.webster.msnotification.constants.EmailTarget;
import com.webster.msnotification.constants.EndpointConstants;
import com.webster.msnotification.dto.EmailTokenDTO;
import com.webster.msnotification.service.EmailTokenSenderService;

import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class EmailNotificationController {
	@NonNull
	private EmailTokenSenderService emailTokenSenderService;

	@PostMapping(EndpointConstants.EMAIL_CONFIRMATION)
	public ResponseEntity<Object> handleEmailConfirmation(@Valid @RequestBody EmailTokenDTO emailTokenDto) {
		emailTokenSenderService.send(emailTokenDto, EmailTarget.CONFIRMATION);
		return ResponseEntity.status(HttpStatus.OK).body(null);
	}
	
	@PostMapping(EndpointConstants.EMAIL_PASSWORD_RESET)
	public ResponseEntity<Object> handleEmailPasswordReset(@Valid @RequestBody EmailTokenDTO emailTokenDto) {
		emailTokenSenderService.send(emailTokenDto, EmailTarget.PASSWORD_RESET);
		return ResponseEntity.status(HttpStatus.OK).body(null);
	}
}
