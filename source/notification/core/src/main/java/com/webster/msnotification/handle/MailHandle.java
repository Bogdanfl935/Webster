package com.webster.msnotification.handle;

import java.io.IOException;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Multipart;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;
import javax.validation.Valid;

import org.springframework.stereotype.Component;

import com.webster.msnotification.constants.RenderingConstants;
import com.webster.msnotification.dto.EmailContentDTO;

import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class MailHandle {
	@NonNull
	private MailSessionProducer mailSessionProducer;

	public MimeMessage composeMimeMessage(@Valid EmailContentDTO emailContentDto)
			throws MessagingException, IOException {
		Session session = mailSessionProducer.produceSession();

		MimeMessage message = new MimeMessage(session);
		message.addRecipient(Message.RecipientType.TO, new InternetAddress(emailContentDto.getDestination()));
		message.setSubject(emailContentDto.getSubject());
		message.setContent(assembleMessageContent(emailContentDto));

		return message;
	}

	public void sendMessage(Message message) throws MessagingException {
		Transport.send(message);
	}

	private Multipart assembleMessageContent(EmailContentDTO emailContentDto) throws MessagingException, IOException {
		Multipart multipart = new MimeMultipart();
		MimeBodyPart textPart = new MimeBodyPart();
		MimeBodyPart imagePart = new MimeBodyPart();

		textPart.setContent(emailContentDto.getContent(), "text/html; charset=utf-8");
		imagePart.attachFile(String.format("%s/%s", RenderingConstants.PATH_TO_STATIC_RESOURCES,
				RenderingConstants.MOTORAGE_LOGO_FILENAME));
		imagePart.setContentID(String.format("<%s>", RenderingConstants.MOTORAGE_LOGO_CID_VALUE));
		imagePart.setDisposition(MimeBodyPart.INLINE);

		multipart.addBodyPart(textPart);
		multipart.addBodyPart(imagePart);
		return multipart;
	}

}
