package com.webster.msauth.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StringUtils;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.context.request.WebRequest;

import com.webster.msauth.constants.ValidationConstants;
import com.webster.msauth.dto.BadRequestResponse;
import com.webster.msauth.dto.ErrorDetailsDTO;

@ControllerAdvice
public class CustomBadRequestHandler {

	@ExceptionHandler(MethodArgumentNotValidException.class)
	@ResponseStatus(HttpStatus.BAD_REQUEST)
	@ResponseBody
	public ResponseEntity<Object> handleException(MethodArgumentNotValidException exception, WebRequest request) {
		List<ErrorDetailsDTO> errorDetails = new ArrayList<>();
		List<FieldError> errors = exception.getBindingResult().getFieldErrors();

		for (FieldError fieldError : errors) {
			String defaultErrorMessage = fieldError.getDefaultMessage();
			String errorMessage = defaultErrorMessage.contains(ValidationConstants.CUSTOM_CONSTRAINT_PREFIX)
					? defaultErrorMessage.replace(ValidationConstants.CUSTOM_CONSTRAINT_PREFIX, "")
					: String.format("%s %s.", StringUtils.capitalize(fieldError.getField()), defaultErrorMessage);
			errorDetails.add(new ErrorDetailsDTO(fieldError.getField(), errorMessage));
		}

		BadRequestResponse response = BadRequestResponse.builder().status(HttpStatus.BAD_REQUEST.value())
				.error(HttpStatus.BAD_REQUEST.getReasonPhrase()).errors(errorDetails)
				.build();

		return new ResponseEntity<Object>(response, new HttpHeaders(), HttpStatus.BAD_REQUEST);
	}

}