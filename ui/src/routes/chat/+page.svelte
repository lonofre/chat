<script lang="ts">
	import { onMount } from 'svelte';
	import { user, websocketChatUrl } from '$lib/store.js';
	import { PUBLIC_API_URL } from '$env/static/public';

	let socket: WebSocket;
	let messagesByGroup: Record<string, { sender: string; text: string }[]> = { all: [] };
	let newMessage = '';
	let groups: { name: string; id: string; color: string; members?: number }[] = [
		{ name: 'all', id: 'all', color: 'indigo', members: 0 }
	];
	let selectedGroup = groups[0];
	let newGroupName = '';

	onMount(() => {
		socket = new WebSocket($websocketChatUrl);
		socket.addEventListener('message', (event) => {
			const data = JSON.parse(event.data);
			const { from, content, group } = data;

			if (!messagesByGroup[group]) {
				messagesByGroup[group] = [];
			}
			messagesByGroup[group] = [...messagesByGroup[group], { sender: from, text: content }];
		});
	});

	async function sendMessage() {
		if (newMessage.trim() === '') return;
		await fetch(`${PUBLIC_API_URL}/message`, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ content: newMessage, from: $user, group: selectedGroup.id })
		});
		newMessage = '';
	}

	async function createOrJoinGroup() {
		if (!newGroupName.trim()) return;
		const groupId = newGroupName.trim().toLowerCase();
		await fetch(`${PUBLIC_API_URL}/group`, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ user: $user, group: groupId })
		});

		if (!groups.find((g) => g.id === groupId)) {
			groups = [...groups, { name: newGroupName, id: groupId, color: 'green' }];
		}
		if (!messagesByGroup[groupId]) messagesByGroup[groupId] = [];
		selectedGroup = groups.find((g) => g.id === groupId);
		newGroupName = '';
	}
</script>

<div class="h-screen flex bg-gray-100 text-gray-800">
	<!-- Sidebar -->
	<aside class="w-80 border-r border-gray-200 bg-white flex flex-col">
		<div class="p-4 border-b border-gray-100">
			<h1 class="text-lg font-semibold">Chats</h1>
			<p class="text-xs text-gray-500">Your recent and group conversations</p>
		</div>

		<div class="p-3">
			<form class="flex gap-2" on:submit|preventDefault={createOrJoinGroup}>
				<input bind:value={newGroupName} placeholder="New chat or group" class="flex-1 px-3 py-2 rounded-full border border-gray-200 text-sm focus:outline-none focus:ring-1 focus:ring-green-300" />
				<button type="submit" class="px-3 py-2 bg-green-500 text-white rounded-full text-sm font-medium">Go</button>
			</form>
		</div>

		<nav class="px-3 py-2 overflow-auto flex-1">
			<ul class="space-y-1">
				{#each groups as g}
					<li>
						<button on:click={() => (selectedGroup = g)} class={`w-full text-left flex items-center gap-3 px-3 py-3 rounded-2xl hover:bg-green-50 transition ${selectedGroup.id === g.id ? 'bg-green-100' : ''}`}>
							<div class={`inline-flex items-center justify-center w-10 h-10 bg-${g.color}-100 text-${g.color}-700 rounded-full font-semibold`}>{g.name[0]}</div>
							<div class="flex-1">
								<div class="text-sm font-medium">{g.name}</div>
								<div class="text-xs text-gray-400 truncate">{messagesByGroup[g.id]?.at(-1)?.text || 'No messages yet'}</div>
							</div>
						</button>
					</li>
				{/each}
			</ul>
		</nav>
	</aside>

	<!-- Main Chat Area -->
	<main class="flex-1 flex flex-col bg-gray-50">
		<!-- Header -->
		<header class="flex items-center justify-between px-6 py-3 border-b border-gray-200 bg-white sticky top-0 z-10">
			<div class="flex items-center gap-3">
				<div class={`inline-flex items-center justify-center w-10 h-10 bg-${selectedGroup.color}-100 text-${selectedGroup.color}-700 rounded-full font-semibold`}>{selectedGroup.name[0]}</div>
				<div>
					<h2 class="text-base font-semibold">{selectedGroup.name}</h2>
					<p class="text-xs text-gray-500">{messagesByGroup[selectedGroup.id]?.length || 0} messages</p>
				</div>
			</div>
		</header>

		<!-- Messages -->
		<section class="flex-1 overflow-auto p-6 space-y-4">
			<div class="max-w-3xl mx-auto flex flex-col gap-4">
				{#each messagesByGroup[selectedGroup.id] || [] as m}
					{#if m.sender === $user}
						<div class="flex flex-col items-end">
							<div class="text-xs text-gray-400 mb-1">{m.sender}</div>
							<div class="max-w-[75%] rounded-2xl rounded-br-none bg-green-500 text-white px-4 py-2 text-sm shadow-sm">{m.text}</div>
						</div>
					{:else}
						<div class="flex flex-col items-start">
							<div class="text-xs text-gray-400 mb-1">{m.sender}</div>
							<div class="max-w-[75%] rounded-2xl rounded-bl-none bg-white border border-gray-200 px-4 py-2 text-sm shadow-sm">{m.text}</div>
						</div>
					{/if}
				{/each}
			</div>
		</section>

		<!-- Input -->
		<footer class="border-t border-gray-200 bg-white p-4 sticky bottom-0">
			<form on:submit|preventDefault={sendMessage} class="max-w-3xl mx-auto flex items-center gap-3">
				<input bind:value={newMessage} placeholder="Message" class="flex-1 px-4 py-3 rounded-full border border-gray-200 focus:outline-none focus:ring-2 focus:ring-green-400 text-sm" />
				<button type="submit" class="p-3 bg-green-500 rounded-full text-white hover:bg-green-600 transition">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12l15-6-6 15-1.5-6L4.5 12z" />
					</svg>
				</button>
			</form>
		</footer>
	</main>
</div>
