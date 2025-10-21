<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';

	let username = '';
	let password = '';
	let success = false;

	async function login() {
		const response = await fetch(`${PUBLIC_API_URL}/register`, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: username,
				password: password
			})
		});
		if (response.ok) {
			username = '';
			password = '';
			success = true;
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-gray-100">
	<div class="w-full max-w-sm p-6 bg-white rounded-2xl shadow-md">
		<!-- Back url -->
		<div class="mt-4 text-left mb-2">
			<a href="/" class="text-sm text-blue-600 hover:text-blue-700 underline hover:no-underline">
				&lt;&lt; Return to login
			</a>
		</div>
		{#if success}
			<!-- Success badge -->
			<div
				class="mt-4 w-full mb-2 inline-flex items-center gap-2 rounded-lg bg-green-50 px-4 py-2 text-sm text-green-700 border border-green-200"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-4 w-4"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M5 13l4 4L19 7"
					/>
				</svg>
				You’ve been registered successfully.
			</div>
		{/if}

		<!-- New account form -->
		<h1 class="text-2xl font-bold mb-6 text-center text-gray-800">Create your account</h1>

		<div class="mb-4">
			<input
				type="text"
				id="username"
				name="username"
				bind:value={username}
				placeholder="Username"
				class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
			/>
		</div>

		<div class="mb-4">
			<input
				type="password"
				id="password"
				name="password"
				bind:value={password}
				placeholder="Password"
				class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
			/>
		</div>

		<button
			on:click={login}
			class="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
		>
			Register
		</button>
	</div>
</div>
