<script>
	let messages = [
		{ sender: "Bot", text: "Hello! How can I help you?" }
	];
	let newMessage = "";

	async function sendMessage() {
		if (newMessage.trim() === "") return;

		const response = await fetch("http://localhost:5163/message", {
			method: "POST",
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({content: newMessage})
		})

		newMessage = "";
	}
</script>

<div class="flex items-center justify-center h-screen bg-gray-100 px-4">
	<div class="flex flex-col w-full max-w-md h-[80vh] p-4 bg-white shadow-md rounded">
		<!-- Scrollable message list -->
		<div
			class="flex-1 overflow-y-auto mb-4 space-y-2 pr-2"
		>
			{#each messages as { sender, text }}
				<div class="flex flex-col">
					<span class="text-sm text-gray-500">{sender}</span>
					<div
						class="p-2 rounded-lg max-w-xs"
						class:bg-blue-100={sender === "You"}
						class:bg-gray-100={sender !== "You"}
					>
						{text}
					</div>
				</div>
			{/each}
		</div>

		<!-- Message input -->
		<form class="flex gap-2" on:submit|preventDefault={sendMessage}>
			<input
				type="text"
				class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
				bind:value={newMessage}
				placeholder="Type a message..."
			/>
			<button
				type="submit"
				class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
				Send
			</button>
		</form>
	</div>
</div>
