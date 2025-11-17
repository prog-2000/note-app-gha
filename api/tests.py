from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Note


class NoteAPITestCase(APITestCase):
	"""API tests for Note CRUD operations."""

	def test_routes(self):
		"""GET /api/ should return a list of routes."""
		res = self.client.get('/api/')
		self.assertEqual(res.status_code, 200)
		self.assertIsInstance(res.data, list)

	def test_create_get_update_delete_note(self):
		# Create a note
		res = self.client.post('/api/notes/create/', {'body': 'hello world'}, format='json')
		self.assertEqual(res.status_code, 200)
		created = res.data
		self.assertIn('id', created)
		note_id = created['id']
		self.assertEqual(created['body'], 'hello world')

		# List notes
		res = self.client.get('/api/notes/')
		self.assertEqual(res.status_code, 200)
		self.assertTrue(isinstance(res.data, list))
		self.assertTrue(any(n['id'] == note_id for n in res.data))

		# Retrieve single note
		res = self.client.get(f'/api/notes/{note_id}/')
		self.assertEqual(res.status_code, 200)
		self.assertEqual(res.data['body'], 'hello world')

		# Update note
		res = self.client.put(f'/api/notes/{note_id}/update/', {'body': 'updated body'}, format='json')
		self.assertEqual(res.status_code, 200)
		self.assertEqual(res.data['body'], 'updated body')

		# Delete note
		res = self.client.delete(f'/api/notes/{note_id}/delete/')
		self.assertEqual(res.status_code, 200)
		# view returns a string message on delete
		self.assertIn('deleted', str(res.data).lower())

		# Ensure the note no longer exists
		exists = Note.objects.filter(id=note_id).exists()
		self.assertFalse(exists)

