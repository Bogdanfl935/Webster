package com.webster.msnotification.dto;


import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;

import org.hibernate.validator.constraints.URL;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
public class EmailTokenDTO {
	@NotBlank
	@Getter
	@Setter
	@URL
	private String targetUrl;
	@NotBlank
	@Getter
	@Setter
	@Email
	private String recipient;
}
