<script>
    let name = "";
    let status = "";

    async function submitForm() {
        const response = await fetch("http://localhost:8080/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, status }),
        });

        const result = await response.json();
        console.log(result);

        alert("Name submitted!")
    }
</script>

<div class="flex flex-col items-center min-h-screen bg-gray-900 text-white p-4">
    <h1 class="text-3xl font-bold mb-6 text-center">NUS Taekwondo Attendance App</h1>
    
    <input
      type="text"
      bind:value={name}
      placeholder="Enter the member's name"
      class="w-full max-w-md p-3 text-lg border border-gray-600 bg-gray-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  
    <div class="mt-6 w-full max-w-md">
      <p class="text-lg mb-3">Member's status:</p>
  
      <label class="flex items-center justify-between p-3 bg-gray-800 rounded-xl cursor-pointer mb-3">
        <span>Regular Student</span>
        <input type="radio" bind:group={status} value="Regular" class="hidden" />
        <div class="w-6 h-6 border-2 border-gray-500 rounded-full flex items-center justify-center">
          {#if status === "Regular"}
            <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
          {/if}
        </div>
      </label>
  
      <label class="flex items-center justify-between p-3 bg-gray-800 rounded-xl cursor-pointer mb-3">
        <span>Alumni</span>
        <input type="radio" bind:group={status} value="Alumni" class="hidden" />
        <div class="w-6 h-6 border-2 border-gray-500 rounded-full flex items-center justify-center">
          {#if status === "Alumni"}
            <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
          {/if}
        </div>
      </label>
  
      <label class="flex items-center justify-between p-3 bg-gray-800 rounded-xl cursor-pointer">
        <span>Exchange Student</span>
        <input type="radio" bind:group={status} value="Exchange" class="hidden" />
        <div class="w-6 h-6 border-2 border-gray-500 rounded-full flex items-center justify-center">
          {#if status === "Exchange"}
            <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
          {/if}
        </div>
      </label>
    </div>
  
    <button
      on:click={submitForm}
      class="mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-all"
    >
      Submit
    </button>
  </div>
