import { Page, Locator } from '@playwright/test';

export class FeedbackComponent {
  readonly page: Page;
  readonly container: Locator;
  readonly commentInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page, messageElement: Locator) {
    this.page = page;
    this.container = messageElement.locator('.feedback-container');
    // These are assumptions based on the user story.
    this.commentInput = this.container.locator('textarea');
    this.submitButton = this.container.locator('button[type="submit"]');
  }

  star(rating: number): Locator {
    // The summary says "for (let i = 1; i <= 5; i++)".
    // The text "Rate this insight: " is in a span before the stars.
    return this.container.locator('.star').nth(rating - 1);
  }

  async rate(rating: number) {
    await this.star(rating).click();
  }

  async submitFeedback(comment?: string) {
    if (comment) {
      await this.commentInput.fill(comment);
    }
    await this.submitButton.click();
  }
}
