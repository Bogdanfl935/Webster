package com.webster.msnotification.renderer;

import org.springframework.stereotype.Component;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;

import com.webster.msnotification.constants.RenderingConstants;

import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class HtmlMailContentRenderer {
	@NonNull
	private TemplateEngine templateEngine;

	public String renderContent(String targetUrl, String contentTemplatePath) {
		Context context = new Context();
		context.setVariable(RenderingConstants.TARGET_URL_VARIABLE, targetUrl);
		context.setVariable(RenderingConstants.LOGO_CID_VARIABLE,
				"cid:" + RenderingConstants.LOGO_CID_VALUE);

		return templateEngine.process(contentTemplatePath, context);
	}
}
