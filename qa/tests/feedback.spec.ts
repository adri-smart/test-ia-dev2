import { test, expect } from '@playwright/test';
import { ChatPage } from '../pages/chat.page';
import { FeedbackComponent } from '../components/feedback.component';

test.describe('KAN-489: [STORY-16] User Feedback Mechanism', () => {
  let chatPage: ChatPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    await chatPage.goto();

    // Pre-condition: get a message from the bot to have feedback on
    await chatPage.sendMessage('What are the total sales?');
    await page.waitForResponse(resp => resp.url().includes('/chat') && resp.status() === 200);
    const botMessage = chatPage.getLastMessageBySender('bot');
    await expect(botMessage).toBeVisible();
  });

  test('should be able to submit feedback with rating', async ({ page }) => {
    const botMessage = chatPage.getLastMessageBySender('bot');
    const feedback = new FeedbackComponent(page, botMessage);

    await expect(feedback.container).toBeVisible();
    // Based on the story, the button is disabled until a rating is given.
    await expect(feedback.submitButton).toBeDisabled();

    await feedback.rate(4);
    await expect(feedback.submitButton).toBeEnabled();

    const feedbackRequestPromise = page.waitForRequest(req => req.url().includes('/feedback') && req.method() === 'POST');
    await feedback.submitFeedback();
    const feedbackRequest = await feedbackRequestPromise;

    const postData = JSON.parse(feedbackRequest.postData() || '{}');
    expect(postData.rating).toBe(4);

    // The story mentions a confirmation message.
    await expect(page.locator('text="Gracias por tu feedback"')).toBeVisible();
  });
});
