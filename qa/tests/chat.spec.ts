import { test, expect } from '@playwright/test';
import { ChatPage } from '../pages/chat.page';

test.describe('KAN-487: [STORY-11] Conversational Interface', () => {
  let chatPage: ChatPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    await chatPage.goto();
  });

  test('should display chat input and send button', async () => {
    await expect(chatPage.chatInput).toBeVisible();
    await expect(chatPage.sendButton).toBeVisible();
  });

  test('should add user message to chat and receive a response', async ({ page }) => {
    const userMessage = 'Hello, agent!';
    
    await chatPage.sendMessage(userMessage);

    // Check user message is displayed
    const lastUserMessage = chatPage.getLastMessageBySender('user');
    await expect(lastUserMessage).toBeVisible();
    await expect(lastUserMessage.locator('p')).toHaveText(userMessage);

    // Wait for and check bot response
    await page.waitForResponse(resp => resp.url().includes('/chat') && resp.status() === 200);
    
    const lastBotMessage = chatPage.getLastMessageBySender('bot');
    await expect(lastBotMessage).toBeVisible();
    await expect(lastBotMessage.locator('p')).not.toBeEmpty();
  });
});
