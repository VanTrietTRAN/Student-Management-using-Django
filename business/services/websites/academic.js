import BaseService from '../base';

class AcademicService extends BaseService {
  get entity() {
    return 'websites';
  }

  // Subjects
  getSubjects(params = null) {
    return this.request().get(`${this.entity}/subjects`, params);
  }

  createSubject(data) {
    return this.request().post(`${this.entity}/subjects`, data);
  }

  updateSubject(id, data) {
    return this.request().put(`${this.entity}/subjects/${id}`, data);
  }

  // Students
  getStudents(params = null) {
    return this.request().get(`${this.entity}/students`, params);
  }

  getStudent(id) {
    return this.request().get(`${this.entity}/students/${id}`);
  }

  // Classrooms
  getClassrooms(params = null) {
    return this.request().get(`${this.entity}/classrooms`, params);
  }

  createStudent(data) {
    return this.request().post(`${this.entity}/students`, data);
  }

  updateStudent(id, data) {
    return this.request().put(`${this.entity}/students/${id}`, data);
  }

  // Registrations
  register(registrationData) {
    return this.request().post(`${this.entity}/registrations/register`, registrationData);
  }

  unregister(id) {
    return this.request().post(`${this.entity}/registrations/${id}/unregister`);
  }

  // Tuitions
  getTuitions(params = null) {
    return this.request().get(`${this.entity}/tuitions`, params);
  }

  payTuition(id) {
    return this.request().post(`${this.entity}/tuitions/${id}/pay`);
  }

  // Grades
  getGrades(params = null) {
    return this.request().get(`${this.entity}/grades`, params);
  }

  createGrade(data) {
    return this.request().post(`${this.entity}/grades`, data);
  }
}

export default new AcademicService();
