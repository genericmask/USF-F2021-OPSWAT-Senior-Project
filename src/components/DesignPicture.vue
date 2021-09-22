<template>
<div>
    <div>
        <label for="endpointIPInput">Enter an Endpoint IP Address: </label>
        <input type="text" id="endpointIPInput" v-model="endpointIP">
        <input type="checkbox" id="endpointAccessInput" v-model="endpointAccessible">
        <label for="endpointAccessInput">Endpoint Is Accessible</label>
        <button @click="submitEndpoint">Submit</button>
    </div>
    <div>
        <span>Endpoints:</span>
        <ul id="endpointList">
            <li v-for="(endpoint, index) in endpoints" :key="index">
                IP: {{endpoint.ip}}, Accessible: {{endpoint.accessible}} <button @click="removeEndpoint(index)">REMOVE</button>
            </li>
        </ul>
    </div>
</div>
</template>

<script>


export default {
    name: "DesignPicture",
    data: function () {
        return {
            endpoints: [],
            endpointIP: "",
            endpointAccessible: true,
        }
    },
    methods: {
        submitEndpoint() {
            if (this.endpointIP.length > 0) {
                this.endpoints.push({
                    ip: this.endpointIP,
                    accessible: this.endpointAccessible
                });
                this.resetEndpointInputs();
            }
        },
        resetEndpointInputs() {
            this.endpointIP = "";
            this.endpointAccessible = true;
        },
        removeEndpoint(endpointsIndex) {
            if (endpointsIndex > -1) {
                this.endpoints.splice(endpointsIndex, 1);
            }
        }
    }
}
</script>

<style scoped>

</style>