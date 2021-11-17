package com.webster.msnotification.service;

import java.io.IOException;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import org.springframework.stereotype.Service;

import com.webster.msnotification.constants.EmailTarget;
import com.webster.msnotification.dto.EmailContentDTO;
import com.webster.msnotification.dto.EmailTokenDTO;
import com.webster.msnotification.exception.EmailDeliveryException;
import com.webster.msnotification.exception.NotificationExceptionMessage;
import com.webster.msnotification.handle.MailHandle;
import com.webster.msnotification.renderer.HtmlMailContentRenderer;

import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class EmailTokenSenderService {
	@NonNull
	private MailHandle mailHandle;
	@NonNull
	private HtmlMailContentRenderer htmlMailContentRenderer;

	public void send(@Valid EmailTokenDTO emailTokenDto, @NotNull EmailTarget emailTarget) {
		String content = htmlMailContentRenderer.renderContent(emailTokenDto.getTargetUrl(),
				emailTarget.getEmailContentTemplatePath());

		EmailContentDTO emailContentDto = EmailContentDTO.builder().destination(emailTokenDto.getRecipient())
				.subject(emailTarget.getEmailSubject()).content(content).build();

		try {
			Message message = mailHandle.composeMimeMessage(emailContentDto);
			mailHandle.sendMessage(message);
		} catch (MessagingException | IOException exception) {
			NotificationExceptionMessage exceptionMessage = NotificationExceptionMessage.EMAIL_DELIVERY_FAILED;
			exceptionMessage.setErrorParameter(emailTokenDto.getRecipient());
			throw new EmailDeliveryException(exceptionMessage.getErrorMessage());
		}
	}
}
