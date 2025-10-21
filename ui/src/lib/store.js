import { writable } from 'svelte/store';

/**
 * Active user.
 */
export const user = writable("");

/**
 * Url used for publish messages in the chat system.
 */
export const websocketChatUrl = writable("");
