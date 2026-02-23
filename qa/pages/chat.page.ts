import { Page, Locator } from '@playwright/test';
import { BasePage } from './base.page';

export class ChatPage extends BasePage {
  readonly chatInput: Locator;
  readonly sendButton: Locator;
  readonly chatMessagesContainer: Locator;

  constructor(page: Page) {
    super(page);
    this.chatInput = page.locator('#chat-input');
    this.sendButton = page.locator('#send-button');
    this.chatMessagesContainer = page.locator('#chat-messages');
  }

  async sendMessage(message: string) {
    await this.chatInput.fill(message);
    await this.sendButton.click();
  }

  getMessageBySender(sender: 'user' | 'bot'): Locator {
    return this.chatMessagesContainer.locator(`.message.${sender}-message`);
  }

  getLastMessageBySender(sender: 'user' | 'bot'): Locator {
    return this.getMessageBySender(sender).last();
  }
}
