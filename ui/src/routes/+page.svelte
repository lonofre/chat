<script lang="ts">
	import { goto } from '$app/navigation';

	let username = "";
	async function login() {
		const response = await fetch("http://localhost:5163/register", {
			method: "POST",
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({name: username})
		})
		if (response.ok){
			await goto("/chat")
		}
	}

</script>

<div class="flex min-h-screen items-center justify-center bg-gray-100">
	<div class="w-full max-w-sm p-6 bg-white rounded-2xl shadow-md">
		<h1 class="text-2xl font-bold mb-6 text-center text-gray-800">Welcome to the chat!</h1>

		<div class="mb-4">
			<label for="username" class="block text-sm font-medium text-gray-700 mb-1">Username:</label>
			<input
				type="text"
				id="username"
				name="username"
				bind:value={username}
				placeholder="Enter your username"
				class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
			/>
		</div>

		<button
			on:click={login}
			class="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
		>
			Login
		</button>
	</div>
</div>