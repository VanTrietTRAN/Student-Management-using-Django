<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Lịch học & thi</h1>
                    <p class="text-gray-600">Quản lý thời khóa biểu, lịch thi và phòng học</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Thêm lịch mới
                </el-button>
            </div>
        </div>

        <!-- Calendar View -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-semibold text-gray-900">Lịch học tuần này</h3>
                <div class="flex gap-2">
                    <el-button @click="previousWeek">Tuần trước</el-button>
                    <el-button type="primary" @click="currentWeek">Tuần này</el-button>
                    <el-button @click="nextWeek">Tuần sau</el-button>
                </div>
            </div>
            
            <!-- Weekly Schedule Table -->
            <div class="overflow-x-auto">
                <table class="w-full border-collapse border border-gray-300">
                    <thead>
                        <tr class="bg-gray-50">
                            <th class="border border-gray-300 p-3 text-left">Thời gian</th>
                            <th class="border border-gray-300 p-3 text-left">Thứ 2</th>
                            <th class="border border-gray-300 p-3 text-left">Thứ 3</th>
                            <th class="border border-gray-300 p-3 text-left">Thứ 4</th>
                            <th class="border border-gray-300 p-3 text-left">Thứ 5</th>
                            <th class="border border-gray-300 p-3 text-left">Thứ 6</th>
                            <th class="border border-gray-300 p-3 text-left">Thứ 7</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="timeSlot in timeSlots" :key="timeSlot.time">
                            <td class="border border-gray-300 p-3 font-medium">{{ timeSlot.time }}</td>
                            <td v-for="day in 6" :key="day" class="border border-gray-300 p-3">
                                <div v-if="getScheduleForTimeSlot(timeSlot.time, day)" 
                                     class="bg-blue-100 p-2 rounded text-sm">
                                    <div class="font-medium">{{ getScheduleForTimeSlot(timeSlot.time, day)?.subject }}</div>
                                    <div class="text-gray-600">{{ getScheduleForTimeSlot(timeSlot.time, day)?.class }}</div>
                                    <div class="text-gray-600">{{ getScheduleForTimeSlot(timeSlot.time, day)?.room }}</div>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Exam Schedule -->
        <div class="bg-white rounded-lg shadow-md p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Lịch thi</h3>
            <div class="overflow-x-auto">
                <el-table :data="examSchedule" stripe style="width: 100%">
                    <el-table-column prop="subjectName" label="Môn thi" width="200" />
                    <el-table-column prop="className" label="Lớp" width="120" />
                    <el-table-column prop="examDate" label="Ngày thi" width="120" />
                    <el-table-column prop="examTime" label="Giờ thi" width="120" />
                    <el-table-column prop="room" label="Phòng thi" width="120" />
                    <el-table-column prop="duration" label="Thời gian" width="120" />
                    <el-table-column prop="teacherName" label="Giám thị" width="200" />
                    <el-table-column label="Thao tác" width="150">
                        <template #default="scope">
                            <el-button size="small" @click="viewExam(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editExam(scope.row)">
                                Sửa
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';

definePageMeta({
    layout: 'websites'
});

const showAddDialog = ref(false);

const timeSlots = ref([
    { time: '7:00 - 8:30' },
    { time: '8:45 - 10:15' },
    { time: '10:30 - 12:00' },
    { time: '13:00 - 14:30' },
    { time: '14:45 - 16:15' },
    { time: '16:30 - 18:00' }
]);

const examSchedule = ref([
    {
        id: 1,
        subjectName: 'Lập trình Cơ bản',
        className: 'CNTT21A',
        examDate: '15/12/2024',
        examTime: '8:00',
        room: 'A101',
        duration: '90 phút',
        teacherName: 'ThS. Nguyễn Văn A'
    },
    {
        id: 2,
        subjectName: 'Cấu trúc dữ liệu',
        className: 'CNTT21B',
        examDate: '16/12/2024',
        examTime: '8:00',
        room: 'A102',
        duration: '90 phút',
        teacherName: 'TS. Trần Thị B'
    }
]);

const getScheduleForTimeSlot = (time: string, day: number) => {
    // Mock data for schedule
    if (time === '7:00 - 8:30' && day === 1) {
        return {
            subject: 'Lập trình Cơ bản',
            class: 'CNTT21A',
            room: 'A101'
        };
    }
    if (time === '8:45 - 10:15' && day === 2) {
        return {
            subject: 'Cấu trúc dữ liệu',
            class: 'CNTT21B',
            room: 'A102'
        };
    }
    return null;
};

const previousWeek = () => {
    ElMessage.info('Chuyển đến tuần trước');
};

const currentWeek = () => {
    ElMessage.info('Chuyển đến tuần hiện tại');
};

const nextWeek = () => {
    ElMessage.info('Chuyển đến tuần sau');
};

const viewExam = (exam: any) => {
    ElMessage.info(`Xem chi tiết lịch thi: ${exam.subjectName}`);
};

const editExam = (exam: any) => {
    ElMessage.info(`Chỉnh sửa lịch thi: ${exam.subjectName}`);
};

const deleteExam = (exam: any) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn xóa lịch thi "${exam.subjectName}"?`,
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(() => {
        const index = examSchedule.value.findIndex(e => e.id === exam.id);
        if (index > -1) {
            examSchedule.value.splice(index, 1);
            ElMessage.success(`Đã xóa lịch thi: ${exam.subjectName}`);
        }
    }).catch(() => {
        ElMessage.info('Đã hủy xóa lịch thi');
    });
};
</script>

<style scoped>
table {
    font-size: 14px;
}
</style>
