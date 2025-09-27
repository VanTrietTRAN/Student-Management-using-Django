<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý môn học</h1>
                    <p class="text-gray-600">Quản lý thông tin môn học, chương trình đào tạo và đăng ký môn học</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Thêm môn học mới
                </el-button>
            </div>
        </div>

        <!-- Search and Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tên môn học..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedMajor" placeholder="Chọn ngành" clearable>
                    <el-option label="Tất cả ngành" value="" />
                    <el-option label="Công nghệ thông tin" value="CNTT" />
                    <el-option label="Kỹ thuật phần mềm" value="KTPM" />
                    <el-option label="An toàn thông tin" value="ATTT" />
                </el-select>
                <el-select v-model="selectedType" placeholder="Loại môn học" clearable>
                    <el-option label="Tất cả loại" value="" />
                    <el-option label="Bắt buộc" value="Bắt buộc" />
                    <el-option label="Tự chọn" value="Tự chọn" />
                    <el-option label="Thực tập" value="Thực tập" />
                </el-select>
                <el-button type="primary" :icon="Search" @click="handleSearch">
                    Tìm kiếm
                </el-button>
            </div>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconFile class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng môn học</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalSubjects }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconFile class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Môn bắt buộc</p>
                        <p class="text-2xl font-bold text-gray-900">{{ requiredSubjects }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconFile class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Môn tự chọn</p>
                        <p class="text-2xl font-bold text-gray-900">{{ electiveSubjects }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconFile class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Môn thực tập</p>
                        <p class="text-2xl font-bold text-gray-900">{{ internshipSubjects }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Subjects Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách môn học</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredSubjects" stripe style="width: 100%">
                    <el-table-column prop="subjectCode" label="Mã môn" width="120" />
                    <el-table-column prop="subjectName" label="Tên môn học" width="250" />
                    <el-table-column prop="credits" label="Tín chỉ" width="100" />
                    <el-table-column prop="major" label="Ngành" width="120" />
                    <el-table-column prop="type" label="Loại" width="120">
                        <template #default="scope">
                            <el-tag :type="getTypeColor(scope.row.type)">
                                {{ scope.row.type }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="semester" label="Học kỳ" width="100" />
                    <el-table-column prop="teacherName" label="Giảng viên" width="200" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewSubject(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editSubject(scope.row)">
                                Sửa
                            </el-button>
                            <el-button size="small" type="danger" @click="deleteSubject(scope.row)">
                                Xóa
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="p-4 border-t border-gray-200">
                <el-pagination
                    v-model:current-page="currentPage"
                    v-model:page-size="pageSize"
                    :page-sizes="[10, 20, 50, 100]"
                    :total="totalSubjects"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Subject Dialog -->
        <el-dialog v-model="showAddDialog" title="Thêm môn học mới" width="600px">
            <el-form :model="newSubject" label-width="120px">
                <el-form-item label="Mã môn học">
                    <el-input v-model="newSubject.subjectCode" />
                </el-form-item>
                <el-form-item label="Tên môn học">
                    <el-input v-model="newSubject.subjectName" />
                </el-form-item>
                <el-form-item label="Số tín chỉ">
                    <el-input-number v-model="newSubject.credits" :min="1" :max="6" />
                </el-form-item>
                <el-form-item label="Ngành">
                    <el-select v-model="newSubject.major" placeholder="Chọn ngành">
                        <el-option label="Công nghệ thông tin" value="CNTT" />
                        <el-option label="Kỹ thuật phần mềm" value="KTPM" />
                        <el-option label="An toàn thông tin" value="ATTT" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Loại môn học">
                    <el-select v-model="newSubject.type" placeholder="Chọn loại">
                        <el-option label="Bắt buộc" value="Bắt buộc" />
                        <el-option label="Tự chọn" value="Tự chọn" />
                        <el-option label="Thực tập" value="Thực tập" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Học kỳ">
                    <el-input-number v-model="newSubject.semester" :min="1" :max="8" />
                </el-form-item>
                <el-form-item label="Giảng viên">
                    <el-input v-model="newSubject.teacherName" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addSubject">Thêm</el-button>
            </template>
        </el-dialog>

        <!-- View Subject Dialog -->
        <el-dialog v-model="showViewDialog" title="Thông tin môn học" width="800px">
            <div v-if="selectedSubject" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Mã môn học</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSubject.subjectCode }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Tên môn học</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSubject.subjectName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Số tín chỉ</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSubject.credits }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Ngành</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSubject.major }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Loại môn học</label>
                        <el-tag :type="getTypeColor(selectedSubject.type)">
                            {{ selectedSubject.type }}
                        </el-tag>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Học kỳ</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSubject.semester }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Giảng viên</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedSubject.teacherName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Trạng thái</label>
                        <el-tag :type="getStatusType(selectedSubject.status)">
                            {{ selectedSubject.status }}
                        </el-tag>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showViewDialog = false">Đóng</el-button>
                <el-button type="primary" @click="editSubjectFromView">Chỉnh sửa</el-button>
            </template>
        </el-dialog>

        <!-- Edit Subject Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa môn học" width="600px">
            <el-form :model="editingSubject" label-width="120px">
                <el-form-item label="Mã môn học">
                    <el-input v-model="editingSubject.subjectCode" disabled />
                </el-form-item>
                <el-form-item label="Tên môn học">
                    <el-input v-model="editingSubject.subjectName" />
                </el-form-item>
                <el-form-item label="Số tín chỉ">
                    <el-input-number v-model="editingSubject.credits" :min="1" :max="6" />
                </el-form-item>
                <el-form-item label="Ngành">
                    <el-select v-model="editingSubject.major" placeholder="Chọn ngành">
                        <el-option label="Công nghệ thông tin" value="CNTT" />
                        <el-option label="Kỹ thuật phần mềm" value="KTPM" />
                        <el-option label="An toàn thông tin" value="ATTT" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Loại môn học">
                    <el-select v-model="editingSubject.type" placeholder="Chọn loại">
                        <el-option label="Bắt buộc" value="Bắt buộc" />
                        <el-option label="Tự chọn" value="Tự chọn" />
                        <el-option label="Thực tập" value="Thực tập" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Học kỳ">
                    <el-input-number v-model="editingSubject.semester" :min="1" :max="8" />
                </el-form-item>
                <el-form-item label="Giảng viên">
                    <el-input v-model="editingSubject.teacherName" />
                </el-form-item>
                <el-form-item label="Trạng thái">
                    <el-select v-model="editingSubject.status" placeholder="Chọn trạng thái">
                        <el-option label="Đang mở" value="Đang mở" />
                        <el-option label="Đã đóng" value="Đã đóng" />
                        <el-option label="Tạm dừng" value="Tạm dừng" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateSubject">Cập nhật</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconFile from '@/assets/icons/file.svg';

definePageMeta({
    layout: 'websites'
});

// Reactive data
const searchKeyword = ref('');
const selectedMajor = ref('');
const selectedType = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedSubject = ref(null);
const editingSubject = ref({});

const newSubject = ref({
    subjectCode: '',
    subjectName: '',
    credits: 3,
    major: '',
    type: '',
    semester: 1,
    teacherName: ''
});

// Mock data
const subjects = ref([
    {
        id: 1,
        subjectCode: 'CS101',
        subjectName: 'Lập trình Cơ bản',
        credits: 3,
        major: 'CNTT',
        type: 'Bắt buộc',
        semester: 1,
        teacherName: 'ThS. Nguyễn Văn A',
        status: 'Đang mở'
    },
    {
        id: 2,
        subjectCode: 'CS102',
        subjectName: 'Cấu trúc dữ liệu',
        credits: 3,
        major: 'CNTT',
        type: 'Bắt buộc',
        semester: 2,
        teacherName: 'TS. Trần Thị B',
        status: 'Đang mở'
    },
    {
        id: 3,
        subjectCode: 'CS201',
        subjectName: 'Lập trình Web',
        credits: 3,
        major: 'KTPM',
        type: 'Tự chọn',
        semester: 3,
        teacherName: 'ThS. Lê Văn C',
        status: 'Đang mở'
    },
    {
        id: 4,
        subjectCode: 'CS301',
        subjectName: 'Thực tập tốt nghiệp',
        credits: 4,
        major: 'ATTT',
        type: 'Thực tập',
        semester: 7,
        teacherName: 'TS. Phạm Thị D',
        status: 'Đang mở'
    }
]);

// Computed properties
const totalSubjects = computed(() => subjects.value.length);
const requiredSubjects = computed(() => subjects.value.filter(s => s.type === 'Bắt buộc').length);
const electiveSubjects = computed(() => subjects.value.filter(s => s.type === 'Tự chọn').length);
const internshipSubjects = computed(() => subjects.value.filter(s => s.type === 'Thực tập').length);

const filteredSubjects = computed(() => {
    let filtered = subjects.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(subject => 
            subject.subjectName.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
            subject.subjectCode.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedMajor.value) {
        filtered = filtered.filter(subject => subject.major === selectedMajor.value);
    }
    
    if (selectedType.value) {
        filtered = filtered.filter(subject => subject.type === selectedType.value);
    }
    
    return filtered;
});

// Methods
const getTypeColor = (type: string) => {
    switch (type) {
        case 'Bắt buộc': return 'danger';
        case 'Tự chọn': return 'success';
        case 'Thực tập': return 'warning';
        default: return 'info';
    }
};

const getStatusType = (status: string) => {
    switch (status) {
        case 'Đang mở': return 'success';
        case 'Đã đóng': return 'info';
        case 'Tạm dừng': return 'warning';
        default: return 'danger';
    }
};

const handleSearch = () => {
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewSubject = (subject: any) => {
    selectedSubject.value = subject;
    showViewDialog.value = true;
};

const editSubject = (subject: any) => {
    editingSubject.value = { ...subject };
    showEditDialog.value = true;
};

const editSubjectFromView = () => {
    showViewDialog.value = false;
    editingSubject.value = { ...selectedSubject.value };
    showEditDialog.value = true;
};

const updateSubject = () => {
    const index = subjects.value.findIndex(s => s.id === editingSubject.value.id);
    if (index > -1) {
        subjects.value[index] = { ...editingSubject.value };
        showEditDialog.value = false;
        ElMessage.success(`Cập nhật thông tin môn học: ${editingSubject.value.subjectName}`);
    }
};

const deleteSubject = (subject: any) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn xóa môn học "${subject.subjectName}"?`,
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(() => {
        const index = subjects.value.findIndex(s => s.id === subject.id);
        if (index > -1) {
            subjects.value.splice(index, 1);
            ElMessage.success(`Đã xóa môn học: ${subject.subjectName}`);
        }
    }).catch(() => {
        ElMessage.info('Đã hủy xóa môn học');
    });
};

const addSubject = () => {
    if (newSubject.value.subjectCode && newSubject.value.subjectName && newSubject.value.major) {
        subjects.value.push({
            id: subjects.value.length + 1,
            ...newSubject.value,
            status: 'Đang mở'
        });
        showAddDialog.value = false;
        newSubject.value = {
            subjectCode: '',
            subjectName: '',
            credits: 3,
            major: '',
            type: '',
            semester: 1,
            teacherName: ''
        };
        ElMessage.success('Thêm môn học thành công');
    } else {
        ElMessage.error('Vui lòng điền đầy đủ thông tin');
    }
};
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
